from dependency_injector import containers, providers

from app.services.auth_service import AuthService


class ServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    repositories = providers.DependenciesContainer()

    auth_service = providers.Factory(
        AuthService,
        auth_repo=repositories.auth_repository,
        user_repo=repositories.user_repository,
    )
