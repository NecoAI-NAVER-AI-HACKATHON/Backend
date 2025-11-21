from dependency_injector import containers, providers

from app.core.dependencies.redis import WorkflowClient


class CustomContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    workflow_client = providers.Factory(
        WorkflowClient,
        config=config,
    )
