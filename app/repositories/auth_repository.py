from app.db.databases.supabase import SupabaseDatabase


class AuthRepository:
    def __init__(self, supabase: SupabaseDatabase):
        self._sb = supabase.get_client()

    def sign_up(self, email: str, password: str):
        '''Call Supabase sign_up, return raw response of Supabase.'''
        res = self._sb.auth.sign_up(
            {
                'email': email,
                'password': password,
            }
        )
        return res

    def sign_in_with_password(self, email: str, password: str):
        '''Call Supabase sign_in_with_password.'''
        res = self._sb.auth.sign_in_with_password(
            {
                'email': email,
                'password': password,
            }
        )
        return res

    def refresh_session(self, refresh_token: str):
        '''Call Supabase refresh_session.'''
        res = self._sb.auth.refresh_session(refresh_token)
        return res

    def sign_out(self, token: str):
        '''Call Supabase admin.sign_out with access token.'''
        res = self._sb.auth.admin.sign_out(token)
        return res
