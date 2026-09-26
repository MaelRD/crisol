import pytest

from crisol.core.config import Settings


def test_settings_read_prefixed_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CRISOL_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("CRISOL_API_PORT", "9000")

    settings = Settings(_env_file=None)  # type: ignore[call-arg]

    assert settings.log_level == "DEBUG"
    assert settings.api_port == 9000


def test_settings_reject_invalid_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CRISOL_LOG_LEVEL", "LOUD")

    with pytest.raises(ValueError):
        Settings(_env_file=None)  # type: ignore[call-arg]
