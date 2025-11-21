from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


class PostgresDatabase:
    '''Lightweight PostgreSQL wrapper exposing engine and session factory.

    Usage:
      pg = PostgresDatabase(dsn)
      with pg.session_factory() as session:
          session.query(...)
    '''

    def __init__(self, database_uri: str, **engine_kwargs: Any) -> None:
        self.database_uri = database_uri
        self.engine: Engine = create_engine(self.database_uri, **engine_kwargs)
        # default sessionmaker configuration - can be adjusted when needed
        self._session_local = sessionmaker(
            bind=self.engine, autocommit=False, autoflush=False
        )

    @contextmanager
    def session_factory(self) -> Generator[Session, None, None]:
        '''Context manager that yields a SQLAlchemy Session and commits/rolls back.

        Repositories in this project expect a callable returning a context manager
        producing a Session (see `app.repositories.base_repository.BaseRepository`).
        '''

        session: Session = self._session_local()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
