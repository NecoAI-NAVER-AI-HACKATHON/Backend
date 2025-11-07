from dependency_injector import containers, providers

from app.services.auth_service import AuthService
from app.services.system_service import SystemService
from app.services.workspace_service import WorkspaceService


class ServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    repositories = providers.DependenciesContainer()

    auth_service = providers.Factory(
        AuthService,
        auth_repo=repositories.auth_repository,
        user_repo=repositories.user_repository,
    )

    workspace_service = providers.Factory(
        WorkspaceService,
        workspace_repo=repositories.workspace_repository,
    )

    system_service = providers.Factory(
        SystemService,
        system_repo=repositories.system_repository,
        workspace_repo=repositories.workspace_repository,
    )
