from fastapi import FastAPI

from app.core.config import settings


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title=settings.title,
        debug=settings.debug,
        root_path=settings.root_path
    )

    return app
