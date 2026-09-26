from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from crisol import __version__
from crisol.core.config import Settings, get_settings

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str
    environment: str


@router.get("/health")
def health(settings: Annotated[Settings, Depends(get_settings)]) -> HealthResponse:
    """Liveness check. Later phases add PostgreSQL and Ollama readiness here."""
    return HealthResponse(
        status="ok", app=settings.app_name, version=__version__, environment=settings.environment
    )
