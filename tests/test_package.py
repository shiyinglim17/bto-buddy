import bto_buddy


def test_package_exposes_version() -> None:
    assert bto_buddy.__version__ == "0.1.0"
