"""Application errors and their HTTP translation.

Services raise ``CrisolError`` subclasses; they know nothing about HTTP.
The API layer maps them to status codes in one place.
"""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class CrisolError(Exception):
    """Base class for expected, domain-level failures."""

    status_code: int = 500
    code: str = "internal_error"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotFoundError(CrisolError):
    status_code = 404
    code = "not_found"


class ValidationError(CrisolError):
    status_code = 422
    code = "validation_error"


class ExternalServiceError(CrisolError):
    """A dependency (PostgreSQL, Ollama, ...) failed or is unreachable."""

    status_code = 503
    code = "external_service_error"


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(CrisolError)
    async def handle_crisol_error(request: Request, exc: CrisolError) -> JSONResponse:
        logger.warning(
            "Request failed",
            extra={"path": request.url.path, "error": exc.code, "detail": exc.message},
        )
        return JSONResponse(
            status_code=exc.status_code, content={"error": exc.code, "detail": exc.message}
        )
