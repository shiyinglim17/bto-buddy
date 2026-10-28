"""Configuration A (direct LLM): response parsing, schema validation and failed inference.
No network: a fake client returns canned responses (architecture §12.2)."""

from __future__ import annotations

import json
from datetime import date
from typing import Any

import pytest

from bto_buddy import generation, pipeline
from bto_buddy.llm import LLMError, LLMResponse, estimate_cost_usd
from bto_buddy.schemas import FinalGuidance, GenerationOutput, UserRequest

REQ = UserRequest(
    request_id="T-1",
    situation_text="Ann (28) and Ben (29) are engaged Singapore Citizens and first-timers.",
    question="What should we prepare first?",
    as_of=date(2026, 11, 1),
)

VALID = {
    "summary": "Start with the HFE letter.",
    "claims": [
        {
            "claim_id": "c1",
            "text": "Apply for an HFE letter.",
            "kind": "preparation_step",
            "cited_fact_ids": [],
        },
        {
            "claim_id": "c2",
            "text": "Check hdb.gov.sg for details.",
            "kind": "caveat",
            "cited_fact_ids": [],
        },
    ],
    "missing_profile_fields": [
        {
            "field": "private_property_interest",
            "needed_for": ["application_requirements"],
            "follow_up_question": "Does either of you own private property?",
        }
    ],
    "profile_conflicts": [],
    "out_of_scope_reasons": [],
}


class FakeClient:
    """Returns (or raises) each scripted item in turn and records the messages it saw."""

    model_id = "openai/gpt-oss-120b"
    temperature = 0.0
    reasoning_effort: str | None = "low"

    def __init__(self, *script: str | LLMError) -> None:
        self.script = list(script)
        self.calls: list[list[dict[str, str]]] = []

    def complete(
        self, messages: list[dict[str, str]], schema_name: str, schema: dict[str, Any]
    ) -> LLMResponse:
        self.calls.append(messages)
        item = self.script.pop(0)
        if isinstance(item, LLMError):
            raise item
        return LLMResponse(item, {"choices": []}, 1000, 400, 50, 1500)


def test_valid_response_parses_into_final_guidance() -> None:
    client = FakeClient(json.dumps(VALID))
    g = pipeline.run_direct(REQ, client)
    assert isinstance(g, FinalGuidance)
    assert g.run.status == "ok" and g.run.llm_calls == 1 and g.run.error is None
    assert [d.claim.claim_id for d in g.claims] == ["c1", "c2"]
    assert g.missing_profile_fields[0].field == "private_property_interest"
    # All four signal lists are always present (REQ-ARC-005).
    assert g.profile_conflicts == [] and g.evidence_gaps == [] and g.out_of_scope_reasons == []
    assert g.run.estimated_cost_usd == estimate_cost_usd(client.model_id, 1000, 400)
    assert g.run.kb_version is None and g.run.rules_version is None


def test_baseline_gets_no_evidence_and_no_labels() -> None:
    client = FakeClient(json.dumps(VALID))
    pipeline.run_direct(REQ, client)
    system, user = client.calls[0]
    assert generation.NO_EVIDENCE in system["content"] and "{evidence}" not in system["content"]
    # Only the request's input fields reach the model.
    assert REQ.situation_text in user["content"] and REQ.question in user["content"]
    for leak in ("key_points", "prohibited", 'fact_id"', "R-HFE", "HFE-VALID"):
        assert leak not in system["content"] + user["content"]


@pytest.mark.parametrize(
    "bad",
    [
        "not json",
        json.dumps({**VALID, "summary": None}),  # wrong type
        json.dumps({k: v for k, v in VALID.items() if k != "claims"}),  # missing field
        json.dumps({**VALID, "claims": [{**VALID["claims"][0], "kind": "out_of_scope"}]}),
        json.dumps({**VALID, "verdict": "eligible"}),  # extra field
    ],
)
def test_invalid_output_retries_once_then_succeeds(bad: str) -> None:
    client = FakeClient(bad, json.dumps(VALID))
    g = pipeline.run_direct(REQ, client)
    assert g.run.status == "ok" and g.run.llm_calls == 2
    retry_msgs = client.calls[1]
    assert retry_msgs[-2] == {"role": "assistant", "content": bad}
    assert "failed validation" in retry_msgs[-1]["content"]


def test_invalid_twice_fails_closed_without_substitution() -> None:
    client = FakeClient("not json", "still not json")
    g = pipeline.run_direct(REQ, client)
    assert g.run.status == "failed" and g.run.llm_calls == 2
    assert g.run.error is not None and g.run.error.startswith("validation")
    assert g.claims == [] and g.summary == pipeline.FAILURE_SUMMARY
    assert g.missing_profile_fields == [] and g.out_of_scope_reasons == []


def test_invented_citations_are_a_validation_failure_in_a() -> None:
    cited = {**VALID, "claims": [{**VALID["claims"][0], "cited_fact_ids": ["HFE-VALID-001"]}]}
    client = FakeClient(json.dumps(cited), json.dumps(cited))
    g = pipeline.run_direct(REQ, client)
    assert g.run.status == "failed" and "cited_fact_ids" in (g.run.error or "")


@pytest.mark.parametrize("kind", ["timeout", "rate_limit", "connection", "api_error", "empty"])
def test_transport_failure_is_recorded_not_retried(kind: Any) -> None:
    client = FakeClient(LLMError(kind, "boom", {"error": {"message": "boom"}}))
    g = pipeline.run_direct(REQ, client)
    assert len(client.calls) == 1
    assert g.run.status == "failed" and g.run.error == f"{kind}: boom"
    assert g.claims == [] and g.run.input_tokens == 0


def test_provider_schema_rejection_retries_with_failed_generation() -> None:
    rejected = LLMError(
        "schema_rejected",
        "json_validate_failed",
        {"error": {"code": "json_validate_failed", "failed_generation": '{"bad": 1}'}},
    )
    client = FakeClient(rejected, json.dumps(VALID))
    g = pipeline.run_direct(REQ, client)
    assert g.run.status == "ok" and g.run.llm_calls == 2
    assert client.calls[1][-2]["content"] == '{"bad": 1}'


def test_coverage_restates_model_out_of_scope_reasons() -> None:
    oos = {
        **VALID,
        "claims": [
            {
                "claim_id": "c1",
                "text": "We do not estimate odds.",
                "kind": "caveat",
                "cited_fact_ids": [],
            }
        ],
        "missing_profile_fields": [],
        "out_of_scope_reasons": [
            {
                "code": "excluded_topic",
                "topic": "ballot_odds",
                "detail": "Ballot odds.",
                "redirect_url": None,
            }
        ],
    }
    g = pipeline.run_direct(REQ, FakeClient(json.dumps(oos)))
    assert g.coverage.status == "out_of_scope"
    both = {**oos, "claims": VALID["claims"]}
    assert pipeline.run_direct(REQ, FakeClient(json.dumps(both))).coverage.status == (
        "partially_in_scope"
    )


def test_strict_schema_is_flat_closed_and_fully_required() -> None:
    schema = generation.strict_json_schema(GenerationOutput)
    assert "$ref" not in json.dumps(schema) and "$defs" not in json.dumps(schema)

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("type") == "object" and "properties" in node:
                assert node["additionalProperties"] is False
                assert set(node["required"]) == set(node["properties"])
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(schema)


def test_render_answer_shows_signals_and_disclaimer() -> None:
    text = pipeline.render_answer(pipeline.run_direct(REQ, FakeClient(json.dumps(VALID))))
    assert "Apply for an HFE letter." in text and "Note: Check hdb.gov.sg" in text
    assert "Does either of you own private property?" in text
    assert pipeline.DISCLAIMER in text
    # Configuration-identifying internals are not rendered (blind scoring).
    assert "pretrained" not in text and "gpt-oss" not in text


# ---- the real OpenAI-compatible client, against a mock transport (no network) -------------
def _client(handler: Any) -> Any:
    import httpx

    from bto_buddy.llm import OpenAICompatibleClient

    return OpenAICompatibleClient(
        api_key="test-key",
        base_url="https://llm.invalid/v1",
        max_retries=0,
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )


def _completion(content: str | None) -> dict[str, Any]:
    return {
        "id": "x",
        "object": "chat.completion",
        "created": 0,
        "model": "openai/gpt-oss-120b",
        "choices": [
            {
                "index": 0,
                "finish_reason": "stop",
                "message": {"role": "assistant", "content": content},
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 5,
            "total_tokens": 15,
            "completion_tokens_details": {"reasoning_tokens": 2},
        },
    }


def test_client_parses_content_and_usage() -> None:
    import httpx

    seen: dict[str, Any] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen.update(json.loads(request.content))
        return httpx.Response(200, json=_completion(json.dumps(VALID)))

    resp = _client(handler).complete([{"role": "user", "content": "hi"}], "s", {"type": "object"})
    assert json.loads(resp.content) == VALID
    assert (resp.input_tokens, resp.output_tokens, resp.reasoning_tokens) == (10, 5, 2)
    # D-067 settings are what is actually sent.
    assert seen["temperature"] == 0 and seen["reasoning_effort"] == "low"
    assert seen["response_format"]["json_schema"]["strict"] is True


@pytest.mark.parametrize(
    ("status", "body", "kind"),
    [
        (
            400,
            {"error": {"code": "json_validate_failed", "failed_generation": "{}"}},
            "schema_rejected",
        ),
        (400, {"error": {"code": "invalid_request", "message": "bad"}}, "api_error"),
        (429, {"error": {"message": "slow down"}}, "rate_limit"),
        (503, {"error": {"message": "unavailable"}}, "api_error"),
    ],
)
def test_client_maps_http_errors(status: int, body: dict[str, Any], kind: str) -> None:
    import httpx

    client = _client(lambda r: httpx.Response(status, json=body))
    with pytest.raises(LLMError) as e:
        client.complete([{"role": "user", "content": "hi"}], "s", {"type": "object"})
    assert e.value.kind == kind


def test_client_maps_timeout_and_empty_content() -> None:
    import httpx

    def timeout(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("slow", request=request)

    with pytest.raises(LLMError) as e:
        _client(timeout).complete([{"role": "user", "content": "hi"}], "s", {})
    assert e.value.kind == "timeout"
    with pytest.raises(LLMError) as e:
        _client(lambda r: httpx.Response(200, json=_completion(None))).complete(
            [{"role": "user", "content": "hi"}], "s", {}
        )
    assert e.value.kind == "empty"


def test_heldout_split_needs_final_flag() -> None:
    from evaluation import run

    with pytest.raises(SystemExit, match="final"):
        run.run("A", "test", None, final=False)
