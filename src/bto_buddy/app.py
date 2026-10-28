"""Streamlit entry point for BTO Buddy.

Run with: uv run streamlit run src/bto_buddy/app.py

Every answer is live inference through `pipeline.run` (configurations A, B and D; D-069,
D-071). The
presets only fill the input boxes; nothing is cached or hard-coded.
"""

from __future__ import annotations

import uuid
from datetime import date

import streamlit as st

from bto_buddy import __version__, pipeline
from bto_buddy.llm import LLMError, OpenAICompatibleClient
from bto_buddy.schemas import FinalGuidance, UserRequest

PRIVACY_NOTICE = (
    "Use fictional details only. Do not enter real names, NRIC numbers or other personal data."
)
# Fictional demo profiles (from the development benchmark, never the held-out set).
PRESETS = {
    "Straightforward first-timer couple": (
        "Wei Ling (28) and Arjun (27) are engaged. Both are Singapore Citizens, have never owned "
        "a flat or taken a housing subsidy, and work full-time with CPF contributions. They have "
        "not started the HFE application.",
        "We want to apply in a BTO launch next year. What should we prepare first?",
    ),
    "Missing information": (
        "Rachel and Jun Hao are engaged. Both are Singapore Citizens and have never owned a flat "
        "or taken a housing subsidy.",
        "Can we apply for a BTO together now?",
    ),
    "Policy misconception": (
        "Clara (27) and Zul (28) are engaged Singapore Citizens and first-timers. They have not "
        "applied for the HFE letter.",
        "We'll get our HFE letter now since it's valid for a year, so we can wait for a launch "
        "next October, right?",
    ),
}
CONFIGS = {
    "D: grounded + claim verification (recommended)": "D",
    "B: grounded in verified HDB facts": "B",
    "A: model knowledge only (baseline)": "A",
}


def show(g: FinalGuidance) -> None:
    if g.run.status == "failed":
        st.error(f"No guidance could be produced: {g.run.error}")
        return
    st.subheader("Summary")
    st.write(g.summary)

    facts = [d for d in g.claims if d.claim.kind == "policy_fact"]
    steps = [
        d
        for d in g.claims
        if d.claim.kind == "preparation_step"
        and not (d.verification and d.verification.outcome == "contradicted")
    ]
    caveats = [d for d in g.claims if d.claim.kind == "caveat"]
    withheld = [d for d in g.claims if d.verification and d.verification.outcome == "contradicted"]
    facts = [d for d in facts if d not in withheld]
    if facts:
        st.subheader("Published requirements")
        for d in facts:
            links = " ".join(f"[source]({u})" for u in d.sources)
            ver = d.verification
            tag = " ✅ verified" if ver and ver.outcome == "supported" else ""
            if ver and ver.outcome == "insufficient_evidence":
                tag = " ⚠️ *unconfirmed by our sources*"
            st.markdown(f"- {d.claim.text}{tag} {links or '*(no verified source)*'}")
    if withheld:
        st.error(f"{len(withheld)} statement(s) were withheld because our sources contradict them.")
    if steps:
        st.subheader("Preparation actions")
        for d in steps:
            st.markdown(f"- {d.claim.text}")
    if g.missing_profile_fields:
        st.subheader("We need more information")
        for m in g.missing_profile_fields:
            st.markdown(f"- {m.follow_up_question} *(field: {m.field.value})*")
    if g.profile_conflicts:
        st.subheader("Contradictory details: please clarify")
        for c in g.profile_conflicts:
            st.warning(f"{c.detail} {c.clarification_question}")
    if g.evidence_gaps:
        st.subheader("Not confirmed by our sources")
        for e in g.evidence_gaps:
            url = f" Check {e.official_source_url}." if e.official_source_url else ""
            st.markdown(f"- {e.detail}{url}")
    if caveats:
        st.subheader("Uncertainty and official confirmation")
        for d in caveats:
            st.markdown(f"- {d.claim.text}")
    if g.out_of_scope_reasons:
        st.subheader("Outside what BTO Buddy covers")
        for o in g.out_of_scope_reasons:
            url = f" See {o.redirect_url}." if o.redirect_url else ""
            st.info(f"{o.detail}{url}")
    if g.visual_resources:
        st.subheader("Official learning resources (links only, not used as evidence)")
        for v in g.visual_resources:
            st.markdown(f"- [{v.title}]({v.url}) ({v.kind})")
    st.caption(
        f"{g.policy_period} · config {g.run.config_id} · {g.run.model_id} · "
        f"{g.run.latency_ms} ms · {g.run.input_tokens}+{g.run.output_tokens} tokens · "
        f"est. ${g.run.estimated_cost_usd or 0:.5f}"
    )


def main() -> None:
    st.set_page_config(page_title="BTO Buddy", layout="centered")
    st.title("BTO Buddy")
    st.caption(f"BTO pre-application preparation assistant · prototype v{__version__}")
    st.warning(pipeline.DISCLAIMER)
    st.info(PRIVACY_NOTICE)

    preset = st.selectbox("Load a demo example (optional)", ["(none)", *PRESETS])
    situation, question = PRESETS.get(preset, ("", ""))
    situation = st.text_area("Your situation (fictional)", value=situation, height=120)
    question = st.text_input("Your question", value=question)
    config = CONFIGS[st.radio("Answer mode", list(CONFIGS))]

    if st.button("Get preparation guidance", type="primary"):
        if not situation.strip() or not question.strip():
            st.error("Please describe your situation and ask a question.")
            return
        try:
            client = OpenAICompatibleClient.from_env()
        except LLMError:
            st.error(
                "No LLM API key is configured. Set BTO_BUDDY_LLM_API_KEY (see .env.example) "
                "and restart."
            )
            return
        request = UserRequest(
            request_id=uuid.uuid4().hex[:8],
            situation_text=situation,
            question=question,
            as_of=date.today(),
        )
        with st.spinner("Preparing guidance..."):
            g = pipeline.run(request, config, client)  # type: ignore[arg-type]
        show(g)


main()
