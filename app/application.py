from fastapi import FastAPI

from app.core.config import settings
from app.api.routers import router


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title=settings.title,
        debug=settings.debug,
        root_path=settings.root_path
    )
    app.include_router(router)

    return app
