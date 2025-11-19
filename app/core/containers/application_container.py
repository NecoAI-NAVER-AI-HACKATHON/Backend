from dependency_injector import containers, providers
import logging
from typing import Mapping, Optional
from app.core.containers.custom_container import CustomContainer
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
            'app.api.endpoints.system_execution',
            'app.core.dependencies.auth_deps',
            'app.core.dependencies.upload_trigger_deps',
        ]
    )

    config = providers.Configuration()
    # Don't import global configs here. Provide configs to the container at runtime
    # by using the `create` helper below or by calling `container.config.from_dict(...)`
    # This keeps the container decoupled from any particular config source and
    # allows tests or different environments to supply their own config dict.

    database = providers.Container(
        DatabaseContainer,
        config=config,
    )

    repositories = providers.Container(
        RepositoryContainer,
        config=config,
        database=database,
    )

    custom_containers = providers.Container(
        CustomContainer,
        config=config,
    )

    services = providers.Container(
        ServiceContainer,
        config=config,
        repositories=repositories,
        custom_containers=custom_containers,
    )

    @classmethod
    def create(cls, config_data: Optional[Mapping] = None) -> "ApplicationContainer":
        """
        Create and return an instance of ApplicationContainer with optional config data.

        Examples:
            from app.configs.app_config import configs
            container = ApplicationContainer.create(configs)

            # or, programmatically
            container = ApplicationContainer.create({"db": {"dsn": "..."}})

        The provided mapping will be loaded into the internal `config` provider via
        `from_dict`, which is compatible with the Dependency Injector `Configuration`.
        """
        container = cls()
        if config_data:
            # load mapping into the Configuration provider
            container.config.from_dict(dict(config_data))
        return container
