"""Smoke test: the package imports and the Streamlit entry point renders without errors."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

import bto_buddy

APP_PATH = Path(__file__).resolve().parents[1] / "src" / "bto_buddy" / "app.py"


def test_app_renders_with_disclaimer() -> None:
    app = AppTest.from_file(str(APP_PATH)).run(timeout=30)

    assert not app.exception
    assert app.title[0].value == "BTO Buddy"
    assert bto_buddy.__version__ in app.caption[0].value
    # The non-assessment disclaimer must always be visible (REQ-PRB-010).
    assert "not an official" in app.warning[0].value
    assert "eligibility assessment" in app.warning[0].value


def test_preset_fills_inputs_and_missing_key_gives_clear_error(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.delenv("BTO_BUDDY_LLM_API_KEY", raising=False)
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    app = AppTest.from_file(str(APP_PATH)).run(timeout=30)
    app.selectbox[0].select("Missing information").run(timeout=30)
    assert "Rachel and Jun Hao" in app.text_area[0].value
    app.button[0].click().run(timeout=30)
    assert not app.exception
    assert any("No LLM API key" in e.value for e in app.error)
