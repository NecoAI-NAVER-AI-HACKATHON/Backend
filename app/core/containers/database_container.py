from dependency_injector import containers, providers
from app.db.factory import create_database


class DatabaseContainer(containers.DeclarativeContainer):
    '''DI container for databases. Creates either Supabase or Postgres helpers
    depending on configuration.
    '''

    config = providers.Configuration()

    # Create a singleton database helper. `create_database` will inspect
    # the config or environment to decide which concrete DB to return.
    supabase_db = providers.Singleton(
        create_database,
        db_type='supabase',
        configs=config,
    )

    postgres_db = providers.Singleton(
        create_database,
        db_type='postgresql',
        configs=config,
        echo=False,
    )
