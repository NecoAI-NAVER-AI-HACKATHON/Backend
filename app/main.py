# app/main.py
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import cast

from fastapi import FastAPI, Response
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import routers
from app.core.config import configs
from app.core.containers.application_container import ApplicationContainer


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def _add_cors(app: FastAPI) -> None:
    """CORS configuration."""
    if configs.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(o) for o in configs.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


def _add_simple_endpoints(app: FastAPI) -> None:
    @app.get("/", include_in_schema=False)
    async def health() -> dict[str, str]:
        return {"message": "Server is working!"}

    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon_no_content():
        return Response(status_code=204)  # No Content


def _include_routes(app: FastAPI) -> None:
    app.include_router(routers, prefix=configs.API_V1_STR)


def _build_container() -> ApplicationContainer:
    container = ApplicationContainer()
    # container.wire(modules=[__name__])
    return container


@asynccontextmanager
async def _lifespan(app: FastAPI):
    logger = logging.getLogger("app.lifespan")
    logger.info("Starting application...")

    container: ApplicationContainer = cast(ApplicationContainer, app.state.container)

    container.init_resources()
    # await container.wire_packages(
    #     packages=["app.api.endpoints", "app.services"]
    # )
    app.state.db = container.database().db  # dependency callable

    try:
        yield
    finally:
        logger.info("Shutting down application...")
        container.shutdown_resources()
        logger.info("Application shutdown complete")


def create_app() -> FastAPI:
    container = _build_container()

    app = FastAPI(
        title=configs.PROJECT_NAME,
        version="0.0.1",
        openapi_url=f"{configs.API}/openapi.json",
        lifespan=_lifespan,
    )
    app.state.container = container

    _add_cors(app)
    _add_simple_endpoints(app)
    _include_routes(app)

    return app


app: FastAPI = create_app()
