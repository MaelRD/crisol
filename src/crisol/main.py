"""FastAPI application factory.

Run with ``uv run uvicorn crisol.main:create_app --factory --reload`` (or ``make dev``).
Using a factory avoids building the app (and reading config) at import time.
"""

import logging
import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response

from crisol import __version__
from crisol.api.routes import health
from crisol.core.config import Settings, get_settings
from crisol.core.exceptions import register_exception_handlers
from crisol.core.logging import configure_logging

logger = logging.getLogger("crisol.api")


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    configure_logging(settings)

    app = FastAPI(title=settings.app_name, version=__version__)
    register_exception_handlers(app)
    app.include_router(health.router)

    @app.middleware("http")
    async def log_requests(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = request.headers.get("x-request-id") or uuid.uuid4().hex[:12]
        start = time.perf_counter()
        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        logger.info(
            "%s %s -> %s",
            request.method,
            request.url.path,
            response.status_code,
            extra={
                "request_id": request_id,
                "duration_ms": round((time.perf_counter() - start) * 1000, 1),
            },
        )
        return response

    logger.info(
        "Application ready", extra={"environment": settings.environment, "version": __version__}
    )
    return app
