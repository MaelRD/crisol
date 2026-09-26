"""Logging setup.

Standard library ``logging`` only. Modules get a logger with
``logging.getLogger(__name__)`` and may attach structured fields through
``extra={...}``; the formatters render those fields so pipeline steps
(document received -> chunks -> embeddings -> retrieval -> LLM) stay readable.
"""

import json
import logging
import sys
from datetime import UTC, datetime
from typing import Any

from crisol.core.config import Settings

# Attributes present on every LogRecord; anything else came from ``extra=``.
_RESERVED = set(logging.makeLogRecord({}).__dict__) | {"message", "asctime", "color_message"}


def _extra_fields(record: logging.LogRecord) -> dict[str, Any]:
    return {k: v for k, v in record.__dict__.items() if k not in _RESERVED}


class TextFormatter(logging.Formatter):
    """Human-friendly: ``12:00:01 INFO  crisol.ingestion | Chunks generated chunks=34``."""

    def __init__(self) -> None:
        super().__init__(
            fmt="%(asctime)s %(levelname)-5s %(name)s | %(message)s", datefmt="%H:%M:%S"
        )

    def format(self, record: logging.LogRecord) -> str:
        line = super().format(record)
        extras = _extra_fields(record)
        if extras:
            line += " " + " ".join(f"{k}={v}" for k, v in extras.items())
        return line


class JsonFormatter(logging.Formatter):
    """One JSON object per line, for when logs are shipped somewhere."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "ts": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            **_extra_fields(record),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str, ensure_ascii=False)


def configure_logging(settings: Settings) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter() if settings.log_format == "json" else TextFormatter())

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(settings.log_level)

    # Let uvicorn propagate to our handler instead of using its own format.
    for name in ("uvicorn", "uvicorn.error"):
        uv_logger = logging.getLogger(name)
        uv_logger.handlers.clear()
        uv_logger.propagate = True
    # Our request middleware already logs each request.
    logging.getLogger("uvicorn.access").disabled = True
