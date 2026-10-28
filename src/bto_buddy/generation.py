"""LLM generation (stage 6) with output validation. Extraction (stage 1) is added with C.

Failure handling (architecture §9):
- schema-invalid output (local Pydantic check, or the provider's strict-schema rejection)
  gets ONE retry that carries the validation error;
- transport failures (timeout, rate limit after the SDK's retries, connection, API error,
  empty content) are not retried here;
- anything still failing returns `output=None` with every attempt recorded. The caller fails
  closed; nothing is substituted or dropped.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError

from bto_buddy.llm import LLMClient, LLMError
from bto_buddy.schemas import GenerationOutput, UserRequest

PROMPT_DIR = Path(__file__).parent / "prompts"
GENERATE_PROMPT = "generate_v1"
SCHEMA_NAME = "bto_guidance"

# Configuration A's policy-sources section: no retrieved passages, facts or rule outputs.
# B-D replace this block with their evidence; the rest of the instructions stay identical
# (D-003 "equivalent task instructions").
NO_EVIDENCE = (
    "None are provided for this request. Rely on your own knowledge of HDB policy, and mark "
    "anything you are unsure of as a caveat. cited_fact_ids must be an empty list."
)

# Keywords outside the strict-mode subset that providers accept; Pydantic still enforces
# them locally after the response arrives.
_UNSUPPORTED_KEYWORDS = {"title", "default", "format", "minLength", "maxLength", "minItems"}


def load_prompt(name: str = GENERATE_PROMPT) -> str:
    return (PROMPT_DIR / f"{name}.md").read_text()


def strict_json_schema(model: type[BaseModel]) -> dict[str, Any]:
    """Flatten a Pydantic model into the strict structured-output subset: no $ref, every
    property required (optional values stay nullable), no additional properties."""
    raw = model.model_json_schema()
    defs = raw.get("$defs", {})

    def walk(node: Any) -> Any:
        if isinstance(node, dict):
            if "$ref" in node:
                return walk(defs[node["$ref"].rsplit("/", 1)[-1]])
            out = {
                k: walk(v)
                for k, v in node.items()
                if k != "$defs" and k not in _UNSUPPORTED_KEYWORDS
            }
            if out.get("type") == "object" and "properties" in out:
                out["required"] = list(out["properties"])
                out["additionalProperties"] = False
            return out
        if isinstance(node, list):
            return [walk(v) for v in node]
        return node

    schema: dict[str, Any] = walk(raw)
    return schema


def build_messages(request: UserRequest, evidence: str) -> list[dict[str, str]]:
    system = load_prompt().replace("{evidence}", evidence)
    user = (
        f"Today's date: {request.as_of.isoformat()}\n\n"
        f"<situation>\n{request.situation_text}\n</situation>\n\n"
        f"<question>\n{request.question}\n</question>"
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


@dataclass
class Attempt:
    """One logical call, as recorded in predictions (raw response kept for audit)."""

    content: str | None
    raw: dict[str, Any]
    input_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: int = 0
    latency_ms: int = 0
    error_kind: str | None = None  # LLMError kind, or "validation"
    error: str | None = None


@dataclass
class GenerationResult:
    output: GenerationOutput | None
    attempts: list[Attempt] = field(default_factory=list)

    @property
    def error(self) -> str | None:
        if self.output is not None or not self.attempts:
            return None
        last = self.attempts[-1]
        return f"{last.error_kind}: {last.error}"


def validate_output(
    content: str, allowed_fact_ids: frozenset[str] | None
) -> tuple[GenerationOutput | None, str | None]:
    """Pydantic check, plus: citations must come from the facts actually provided (A has none,
    so any citation there is invented). `None` skips the citation check (the D verifier
    handles out-of-bundle citations instead)."""
    try:
        out = GenerationOutput.model_validate_json(content)
    except ValidationError as e:
        return None, str(e)
    if allowed_fact_ids is not None:
        bad = sorted({f for c in out.claims for f in c.cited_fact_ids if f not in allowed_fact_ids})
        if bad:
            return None, f"cited_fact_ids not among the provided facts: {bad}"
    return out, None


def generate(
    request: UserRequest,
    client: LLMClient,
    *,
    evidence: str = NO_EVIDENCE,
    allowed_fact_ids: frozenset[str] | None = frozenset(),
) -> GenerationResult:
    messages = build_messages(request, evidence)
    schema = strict_json_schema(GenerationOutput)
    result = GenerationResult(output=None)
    for attempt_no in (1, 2):
        try:
            resp = client.complete(messages, SCHEMA_NAME, schema)
        except LLMError as e:
            result.attempts.append(Attempt(None, e.raw, error_kind=e.kind, error=e.detail))
            if e.kind != "schema_rejected" or attempt_no == 2:
                return result
            retry_content = _failed_generation(e.raw)
            err = e.detail
        else:
            out, err_or_none = validate_output(resp.content, allowed_fact_ids)
            result.attempts.append(
                Attempt(
                    resp.content,
                    resp.raw,
                    resp.input_tokens,
                    resp.output_tokens,
                    resp.reasoning_tokens,
                    resp.latency_ms,
                    error_kind=None if out else "validation",
                    error=err_or_none,
                )
            )
            if out is not None:
                result.output = out
                return result
            retry_content, err = resp.content, err_or_none or ""
        # One bounded retry with the error message (architecture §9); never a loop.
        messages = [
            *messages,
            {"role": "assistant", "content": retry_content},
            {
                "role": "user",
                "content": f"That output failed validation:\n{err[:1500]}\n"
                "Return corrected JSON that matches the schema.",
            },
        ]
    return result


def _failed_generation(raw: dict[str, Any]) -> str:
    """The rejected text, when the provider returns it (Groq: error.failed_generation)."""
    err = raw.get("error", raw)
    if isinstance(err, dict) and isinstance(err.get("failed_generation"), str):
        return str(err["failed_generation"])
    return json.dumps(raw)[:2000]
