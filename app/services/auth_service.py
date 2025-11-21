import uuid
from fastapi import HTTPException, status

from app.models.user import User
from app.repositories.auth_repository import AuthRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import (
    SignupRequest,
    SignupResponse,
    LoginRequest,
    LoginResponse,
    RefreshRequest,
    RefreshResponse,
    LogoutResponse,
)


class AuthService:
    def __init__(self, auth_repo: AuthRepository, user_repo: UserRepository):
        self._auth_repo = auth_repo
        self._user_repo = user_repo

    def sign_up(self, payload: SignupRequest) -> SignupResponse:
        try:
            res = self._auth_repo.sign_up(payload.email, payload.password)
            if not res.user or not res.session:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Signup failed.',
                )

            new_user = User(
                id=uuid.UUID(res.user.id),
                email=payload.email,
                role=payload.role or 'user',
            )

            saved_user = self._user_repo.create(new_user)
            if not saved_user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail='Create user failed.',
                )

            return SignupResponse(
                user=res.user.model_dump() if res.user else None,
                session=res.session.model_dump() if res.session else None,
                message='Signed up successfully.',
            )
        except Exception as e:
            # Supabase throws AuthApiError
            raise HTTPException(status_code=400, detail=str(e))

    def login(self, payload: LoginRequest) -> LoginResponse:
        try:
            res = self._auth_repo.sign_in_with_password(payload.email, payload.password)

            if not res.session or not res.session.access_token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Login failed.',
                )

            return LoginResponse(
                access_token=res.session.access_token,
                refresh_token=res.session.refresh_token,
                user=res.user.model_dump() if res.user else {},
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))

    def refresh(self, payload: RefreshRequest) -> RefreshResponse:
        try:
            res = self._auth_repo.refresh_session(payload.refresh_token)

            if not res.session or not res.session.access_token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid refresh token.',
                )

            return RefreshResponse(
                access_token=res.session.access_token,
                refresh_token=res.session.refresh_token,
                user=res.user.model_dump() if res.user else {},
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))

    def logout(self, token: str) -> LogoutResponse:
        try:
            self._auth_repo.sign_out(token)
            return LogoutResponse(message='Logged out successfully.')
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
