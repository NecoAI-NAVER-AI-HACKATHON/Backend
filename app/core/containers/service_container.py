from dependency_injector import containers, providers

from app.services.auth_service import AuthService
from app.services.node_definition_service import NodeDefinitionService
from app.services.system_service import SystemService
from app.services.workspace_service import WorkspaceService
from app.services.system_execution_service import SystemExecutionService


class ServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    repositories = providers.DependenciesContainer()
    custom_containers = providers.DependenciesContainer()

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

    system_execution_service = providers.Factory(
        SystemExecutionService,
        execution_repo=repositories.system_execution_repository,
        system_repo=repositories.system_repository,
        workflow_client=custom_containers.workflow_client,
    )

    node_definition_service = providers.Singleton(
        NodeDefinitionService,
        node_definition_repo=repositories.node_definition_repository,
    )
