from dependency_injector import containers, providers

from app.repositories.auth_repository import AuthRepository
from app.repositories.user_repository import UserRepository


class RepositoryContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    database = providers.DependenciesContainer()

    auth_repository = providers.Factory(
        AuthRepository,
        supabase=database.supabase_db,
    )

    # UserRepository expects a session_factory callable that yields SQLAlchemy Session.
    # When the configured database is PostgreSQL the factory returns a PostgresDatabase
    # which exposes `.session_factory`. We reference that attribute via `provided` so
    # DI wiring will inject the attribute when available.
    user_repository = providers.Factory(
        UserRepository,
        session_factory=database.postgres_db.provided.session_factory,
    )
