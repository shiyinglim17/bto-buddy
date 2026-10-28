"""Streamlit entry point for BTO Buddy.

Run with: uv run streamlit run src/bto_buddy/app.py

The guidance pipeline is not wired in yet. This page shows only what exists, so the
write-up never claims features the code lacks (REQ-DOC-004).
"""

import streamlit as st

from bto_buddy import __version__

DISCLAIMER = (
    "BTO Buddy gives preparation guidance based on published HDB information. "
    "It is not an official eligibility assessment. Always confirm with official HDB services."
)
PRIVACY_NOTICE = (
    "Use fictional details only. Do not enter real names, NRIC numbers or other personal data."
)


def main() -> None:
    st.set_page_config(page_title="BTO Buddy", layout="centered")
    st.title("BTO Buddy")
    st.caption(f"BTO pre-application preparation assistant · prototype v{__version__}")
    st.warning(DISCLAIMER)
    st.info(PRIVACY_NOTICE)
    st.write("The guidance pipeline is under development and not yet available in this build.")


main()
