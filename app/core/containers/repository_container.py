from dependency_injector import containers, providers

from app.repositories.auth_repository import AuthRepository
from app.repositories.node_definition_repository import NodeDefinitionRepository
from app.repositories.system_repository import SystemRepository
from app.repositories.user_repository import UserRepository
from app.repositories.workspace_repository import WorkspaceRepository
from app.repositories.system_execution_repository import SystemExecutionRepository


class RepositoryContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    database = providers.DependenciesContainer()

    auth_repository = providers.Factory(
        AuthRepository,
        supabase=database.supabase_db,
    )

    # Repository expects a session_factory callable that yields SQLAlchemy Session.
    # When the configured database is PostgreSQL the factory returns a PostgresDatabase
    # which exposes `.session_factory`. We reference that attribute via `provided` so
    # DI wiring will inject the attribute when available.
    user_repository = providers.Factory(
        UserRepository,
        session_factory=database.postgres_db.provided.session_factory,
    )

    workspace_repository = providers.Factory(
        WorkspaceRepository,
        session_factory=database.postgres_db.provided.session_factory,
    )

    system_repository = providers.Factory(
        SystemRepository,
        session_factory=database.postgres_db.provided.session_factory,
    )

    system_execution_repository = providers.Factory(
        SystemExecutionRepository,
        session_factory=database.postgres_db.provided.session_factory,
    )

    node_definition_repository = providers.Singleton(
        NodeDefinitionRepository,
        session_factory=database.postgres_db.provided.session_factory,
    )
