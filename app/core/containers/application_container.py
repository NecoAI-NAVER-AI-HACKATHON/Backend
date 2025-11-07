from dependency_injector import containers, providers
import logging
from app.core.config import configs
from app.core.containers.database_container import DatabaseContainer
from app.core.containers.repository_container import RepositoryContainer
from app.core.containers.service_container import ServiceContainer


class ApplicationContainer(containers.DeclarativeContainer):
    logger = logging.getLogger(__name__)

    wiring_config = containers.WiringConfiguration(
        modules=[
            'app.api.endpoints.auth',
            'app.api.endpoints.user',
            'app.api.endpoints.workspace',
            'app.api.endpoints.system',
            'app.core.dependencies.auth_deps',
        ]
    )

    config = providers.Configuration()
    config.override(configs.model_dump())

    database = providers.Container(
        DatabaseContainer,
        config=config,
    )

    repositories = providers.Container(
        RepositoryContainer,
        config=config,
        database=database,
    )

    services = providers.Container(
        ServiceContainer,
        config=config,
        repositories=repositories,
    )
