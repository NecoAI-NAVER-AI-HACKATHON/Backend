'''Supabase database client wrapper.

Provides a small helper class around the official Supabase Python client.

This keeps the rest of the application decoupled from the concrete
Supabase client API and centralizes initialization (URL/key) and
some common operations.
'''

import os
import logging
from typing import Any, Dict, Optional

from supabase import create_client, Client

logger = logging.getLogger(__name__)


class Database:
    '''Lightweight Supabase client wrapper.

    Initialization:
      Database()  # reads SUPABASE_URL and SUPABASE_ANON_KEY from env
      Database(url, key)  # explicit

    Methods provided:
      - table(table_name) -> low-level table proxy (supabase.table)
      - select / insert / update / delete convenience wrappers returning the raw response
      - auth_sign_in / auth_sign_out helpers

    The methods return the supabase response object (dictionary-like) so callers
    can inspect status_code, data, error as needed.
    '''

    def __init__(self, url: Optional[str] = None, key: Optional[str] = None) -> None:
        self.url = url or os.getenv('SUPABASE_URL')
        self.key = key or os.getenv('SUPABASE_ANON_KEY')

        if not self.url or not self.key:
            raise RuntimeError(
                'SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment or passed to Database()'
            )

        self.client = create_client(self.url, self.key)

    def get_client(self) -> Client:
        '''Return the underlying Supabase client instance.'''
        return self.client

    def table(self, table_name: str):
        '''Return the low-level table proxy from the supabase client.

        Use this for advanced queries not covered by the convenience wrappers.
        '''

        return self.client.table(table_name)

    def select(self, table_name: str, columns: str = '*') -> Any:
        '''Select rows from a table.

        Returns the supabase response (usually dict-like with 'data' and 'error').
        '''

        return self.client.table(table_name).select(columns).execute()

    def insert(
        self, table_name: str, payload: Any, returning: Optional[str] = 'representation'
    ) -> Any:
        '''Insert a row or list of rows into a table.

        `payload` can be a dict or a list of dicts. `returning` follows Supabase API
        (e.g. 'representation' to return inserted row(s)).
        '''

        q = self.client.table(table_name).insert(payload)
        if returning:
            q = q.returning(returning)
        return q.execute()

    def update(
        self, table_name: str, payload: Dict[str, Any], match: Dict[str, Any]
    ) -> Any:
        '''Update rows in `table_name` matching the `match` mapping.

        `match` is a simple equality mapping; multiple keys will be ANDed.
        '''

        q = self.client.table(table_name)
        for k, v in match.items():
            q = q.eq(k, v)
        return q.update(payload).execute()

    def delete(self, table_name: str, match: Dict[str, Any]) -> Any:
        '''Delete rows matching `match` mapping.'''

        q = self.client.table(table_name)
        for k, v in match.items():
            q = q.eq(k, v)
        return q.delete().execute()

    # --- Auth helpers ---
    def auth_sign_in(self, email: str, password: str) -> Any:
        '''Sign in a user using email/password.

        Attempts to use modern `sign_in_with_password` API and falls back to
        older `sign_in` if needed.
        '''

        auth = getattr(self.client, 'auth', None)
        if auth is None:
            raise RuntimeError('Supabase client has no auth property')

        # preferred newer method
        if hasattr(auth, 'sign_in_with_password'):
            return auth.sign_in_with_password({'email': email, 'password': password})

        # fallback
        if hasattr(auth, 'sign_in'):
            return auth.sign_in(email=email, password=password)

        raise RuntimeError('No known sign-in method available on supabase auth client')

    def auth_sign_out(self) -> Any:
        '''Sign out the current session (if supported).

        Not all client versions expose the same API; this calls `auth.sign_out()` if present.
        '''

        auth = getattr(self.client, 'auth', None)
        if auth is None or not hasattr(auth, 'sign_out'):
            logger.debug('supabase auth.sign_out not available on this client')
            return None
        return auth.sign_out()
