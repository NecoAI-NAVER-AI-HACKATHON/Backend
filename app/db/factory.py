'''Database factory producing Supabase or PostgreSQL database helpers.

This module exposes `create_database()` which returns either an instance of
the `SupabaseDatabase` or a `PostgresDatabase`

Selection order:
 - explicit `db_type` argument
 - environment variable `DB` or `DB_ENGINE`
 - provided `configs` object (if it has `.DB` / `.DB_ENGINE`)
 - default: 'supabase'
'''

from __future__ import annotations

from typing import Any, Optional

from app.db.databases.postgres import PostgresDatabase
from app.db.databases.supabase import SupabaseDatabase


def create_database(
    db_type: Optional[str] = None, configs: Optional[Any] = None, **kwargs
) -> Any:
    '''Factory that returns a database helper based on `db_type`.

    - For `supabase`: returns an instance of `app.db.databases.supabase.SupabaseDatabase`.
    - For `postgresql`: returns an instance of `app.db.databases.postgres.PostgresDatabase`.

    Additional keyword arguments are passed to the underlying constructors
    (e.g. SQLAlchemy engine kwargs).
    '''

    if db_type in ('supabase', 'supabase-db', 'supabase_database'):
        # supabase DB helper expects SUPABASE_URL and SUPABASE_ANON_KEY in env or passed explicitly
        url = configs['SUPABASE_URL'] if configs else None
        key = configs['SUPABASE_ANON_KEY'] if configs else None

        if not url or not key:
            raise RuntimeError(
                'SUPABASE_URL and SUPABASE_ANON_KEY must be provided for SupabaseDatabase. '
                'Set them in configs or environment variables.'
            )

        return SupabaseDatabase(url=url, key=key)

    if db_type in ('postgresql', 'postgres', 'postgres-db'):
        # locate DATABASE_URI from configs or environment
        database_uri = configs['DATABASE_URI'] if configs else None

        if not database_uri:
            raise RuntimeError(
                'DATABASE_URI not found for PostgreSQL. Provide DATABASE_URI env or configs.DATABASE_URI'
            )

        return PostgresDatabase(database_uri, **kwargs)

    raise ValueError(
        f'Unknown db_type "{db_type}". Supported: "supabase", "postgresql"'
    )
