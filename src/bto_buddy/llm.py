"""The single LLM seam (architecture §11.2, D-041): client protocol, OpenAI-compatible client,
typed failures and token/cost accounting. Only `generation` (and later `verification`) import
this module; tests inject a fake that satisfies `LLMClient`.

The model and settings are fixed by D-067. Configuration comes from the environment only:
  BTO_BUDDY_LLM_API_KEY   (falls back to GROQ_API_KEY)
  BTO_BUDDY_LLM_BASE_URL  (default: Groq's OpenAI-compatible endpoint)
  BTO_BUDDY_LLM_MODEL     (default: openai/gpt-oss-120b)
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, Protocol

import openai
from openai.types.chat import ChatCompletion

# D-067 fixed model and settings. Changing any of these changes every configuration at once.
DEFAULT_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = "openai/gpt-oss-120b"
TEMPERATURE = 0.0
REASONING_EFFORT = "low"
# 4096 (was 6000 in the saved dev runs): Groq counts this cap towards the 8K tokens-per-minute
# limit, so 6000 + a ~2.6K-token B prompt was rejected with HTTP 413 (DEV-12). Observed
# outputs never exceeded ~1.1K tokens.
MAX_COMPLETION_TOKENS = 4096
TIMEOUT_S = 60.0  # per HTTP attempt; Groq answered in ~2 s in model selection
# SDK retries (429 and 5xx, honouring retry-after): the 8K tokens-per-minute plan limit makes
# 429s routine during evaluation runs, and a throttled call is not a model failure.
MAX_TRANSPORT_RETRIES = 8

# USD per 1M tokens (input, output), paid list price checked 2026-10-29 (D-067). Reasoning
# tokens are billed as output. Unknown models get no estimate rather than a guessed one.
PRICES: dict[str, tuple[float, float]] = {"openai/gpt-oss-120b": (0.15, 0.60)}

ErrorKind = Literal["timeout", "rate_limit", "connection", "api_error", "schema_rejected", "empty"]


class LLMError(Exception):
    """A failed call. `raw` keeps whatever the provider returned, for the run record."""

    def __init__(self, kind: ErrorKind, detail: str, raw: dict[str, Any] | None = None) -> None:
        super().__init__(f"{kind}: {detail}")
        self.kind = kind
        self.detail = detail
        self.raw = raw or {}


@dataclass(frozen=True)
class LLMResponse:
    content: str
    raw: dict[str, Any]
    input_tokens: int
    output_tokens: int  # includes reasoning tokens
    reasoning_tokens: int
    latency_ms: int


class LLMClient(Protocol):
    model_id: str
    temperature: float
    reasoning_effort: str | None

    def complete(
        self, messages: list[dict[str, str]], schema_name: str, schema: dict[str, Any]
    ) -> LLMResponse:
        """Return schema-constrained JSON text, or raise LLMError."""
        ...


def estimate_cost_usd(model_id: str, input_tokens: int, output_tokens: int) -> float | None:
    if model_id not in PRICES:
        return None
    p_in, p_out = PRICES[model_id]
    return (input_tokens * p_in + output_tokens * p_out) / 1e6


def read_env(name: str, env_file: Path | None = None) -> str | None:
    """Environment first, then a simple KEY=VALUE `.env` file (no python-dotenv dependency)."""
    # `docker run --env-file` keeps quotes literally (KEY="x" arrives as "x" with quotes), so
    # environment values get the same quote stripping as the .env parser below.
    value = os.environ.get(name, "").strip().strip("'\"")
    if value:
        return value
    if env_file is not None and env_file.exists():
        for line in env_file.read_text().splitlines():
            key, sep, value = line.partition("=")
            if sep and key.strip() == name and value.strip():
                return value.strip().strip("'\"")
    return None


@dataclass
class OpenAICompatibleClient:
    api_key: str = field(repr=False)
    model_id: str = DEFAULT_MODEL
    base_url: str = DEFAULT_BASE_URL
    temperature: float = TEMPERATURE
    reasoning_effort: str | None = REASONING_EFFORT
    max_completion_tokens: int = MAX_COMPLETION_TOKENS
    timeout_s: float = TIMEOUT_S
    max_retries: int = MAX_TRANSPORT_RETRIES
    http_client: Any = field(default=None, repr=False)  # test seam (httpx mock transport)

    @classmethod
    def from_env(cls, env_file: Path | None = None) -> OpenAICompatibleClient:
        key = read_env("BTO_BUDDY_LLM_API_KEY", env_file) or read_env("GROQ_API_KEY", env_file)
        if not key:
            raise LLMError("api_error", "no API key: set BTO_BUDDY_LLM_API_KEY")
        return cls(
            api_key=key,
            model_id=read_env("BTO_BUDDY_LLM_MODEL", env_file) or DEFAULT_MODEL,
            base_url=read_env("BTO_BUDDY_LLM_BASE_URL", env_file) or DEFAULT_BASE_URL,
        )

    def complete(
        self, messages: list[dict[str, str]], schema_name: str, schema: dict[str, Any]
    ) -> LLMResponse:
        client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout_s,
            max_retries=self.max_retries,
            http_client=self.http_client,
        )
        # One plain kwargs dict: provider-specific values (e.g. Groq's reasoning_effort) need not
        # match the SDK's OpenAI-only type overloads.
        kwargs: dict[str, Any] = {
            "model": self.model_id,
            "messages": messages,
            "temperature": self.temperature,
            "max_completion_tokens": self.max_completion_tokens,
            "response_format": {
                "type": "json_schema",
                "json_schema": {"name": schema_name, "strict": True, "schema": schema},
            },
        }
        if self.reasoning_effort is not None:
            kwargs["reasoning_effort"] = self.reasoning_effort
        t0 = time.perf_counter()
        try:
            resp: ChatCompletion = client.chat.completions.create(**kwargs)
        except openai.APITimeoutError as e:
            raise LLMError("timeout", str(e)) from e
        except openai.RateLimitError as e:
            raise LLMError("rate_limit", str(e), _body(e)) from e
        except openai.APIConnectionError as e:
            raise LLMError("connection", str(e)) from e
        except openai.BadRequestError as e:
            body = _body(e)
            # Groq checks strict-schema output server-side and rejects it with this code
            # (seen in model selection); that is a structured-output failure, not transport.
            kind: ErrorKind = (
                "schema_rejected" if "json_validate_failed" in str(body) else "api_error"
            )
            raise LLMError(kind, str(e), body) from e
        except openai.APIStatusError as e:
            raise LLMError("api_error", str(e), _body(e)) from e
        latency_ms = round((time.perf_counter() - t0) * 1000)
        raw = resp.model_dump(mode="json")
        choice = resp.choices[0] if resp.choices else None
        content = choice.message.content if choice else None
        if not content:
            reason = choice.finish_reason if choice else "no choices"
            raise LLMError("empty", f"no content (finish_reason={reason})", raw)
        usage = resp.usage
        details = usage.completion_tokens_details if usage else None
        return LLMResponse(
            content=content,
            raw=raw,
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0,
            reasoning_tokens=(details.reasoning_tokens or 0) if details else 0,
            latency_ms=latency_ms,
        )


def _body(e: openai.APIStatusError) -> dict[str, Any]:
    body = e.body
    return body if isinstance(body, dict) else {"body": body}
