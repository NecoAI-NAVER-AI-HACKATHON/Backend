from dependency_injector import containers, providers
import logging
from app.core.config import configs
from app.core.containers.database_container import DatabaseContainer
from app.core.containers.service_container import ServiceContainer


class ApplicationContainer(containers.DeclarativeContainer):
    logger = logging.getLogger(__name__)

    config = providers.Configuration()
    config.override(configs.model_dump())

    database = providers.Container(
        DatabaseContainer,
        config=config,
    )

    services = providers.Container(
        ServiceContainer,
        config=config,
    )
