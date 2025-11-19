'''Object-oriented application builder for the FastAPI app.

This moves the procedural functions from `app/main.py` into an
`Application` class so the app creation is easier to test and extend.
'''

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Response
from starlette.middleware.cors import CORSMiddleware
from redis import asyncio as aioredis

from app.api.routes import routers
from app.configs.app_config import configs
from app.core.containers.application_container import ApplicationContainer


class Application:
    '''Build and configure the FastAPI application in an OOP style.

    Usage:
      app = Application().create_app()
    '''

    logger = logging.getLogger(__name__)

    def __init__(self, configs_obj=None) -> None:
        self.configs = configs_obj or configs
        self.container: Optional[ApplicationContainer] = None

    def _add_cors(self, app: FastAPI) -> None:
        '''Apply CORS middleware based on configuration.'''

        if self.configs.BACKEND_CORS_ORIGINS:
            app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(o) for o in self.configs.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=['*'],
                allow_headers=['*'],
            )

    def _add_simple_endpoints(self, app: FastAPI) -> None:
        @app.get('/', include_in_schema=False)
        async def health() -> dict[str, str]:
            return {'message': 'Server is working!'}

        @app.get('/favicon.ico', include_in_schema=False)
        async def favicon_no_content():
            return Response(status_code=204)

    def _include_routes(self, app: FastAPI) -> None:
        app.include_router(routers, prefix=self.configs.API_V1_STR)

    def _build_container(self) -> ApplicationContainer:
        container = ApplicationContainer.create(config_data=self.configs.model_dump())
        # wire local modules if required by the container
        container.wire(modules=[__name__])
        return container

    @asynccontextmanager
    async def _lifespan(self, app: FastAPI):
        logger = logging.getLogger('app.lifespan')
        logger.info('Starting application...')

        # initialize container and resources
        if self.container is None:
            self.container = self._build_container()

        self.container.init_resources()
        app.state.container = self.container
        # keep backward-compatible shortcut used elsewhere
        try:
            yield
        finally:
            logger.info('Shutting down application...')
            self.container.shutdown_resources()
            logger.info('Application shutdown complete')

    def create_app(self) -> FastAPI:
        '''Create and return a configured FastAPI app instance.'''

        # build container eagerly so it can be referenced during app lifetime
        self.container = self._build_container()

        app = FastAPI(
            title=self.configs.PROJECT_NAME,
            version='0.0.1',
            openapi_url=f'{self.configs.API}/openapi.json',
            lifespan=self._lifespan,
        )
        redis = aioredis.from_url(
            configs.REDIS_URL, encoding="utf-8", decode_responses=True
        )
        app.state.redis = redis

        self._add_cors(app)
        self._add_simple_endpoints(app)
        self._include_routes(app)

        return app
