from dependency_injector import containers, providers
from app.db.database import Database


class DatabaseContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Singleton(
        Database,
        url=config.SUPABASE_URL,
        key=config.SUPABASE_ANON_KEY,
    )
