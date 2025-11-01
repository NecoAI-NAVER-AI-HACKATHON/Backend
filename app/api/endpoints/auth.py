from fastapi import APIRouter, HTTPException, status
from supabase import create_client, Client
from app.core.config import configs
from app.schemas.auth_schema import (
    SignupRequest,
    SignupResponse,
    LoginRequest,
    LoginResponse,
    RefreshRequest,
    RefreshResponse,
)

router = APIRouter(prefix='/auth', tags=['auth'])


def supabase_client_user() -> Client:
    # Use ANON KEY for user actions: signup/login/refresh
    return create_client(configs.SUPABASE_URL, configs.SUPABASE_ANON_KEY)


@router.post(
    '/signup', response_model=SignupResponse, status_code=status.HTTP_201_CREATED
)
def signup(payload: SignupRequest):
    sb = supabase_client_user()
    try:
        res = sb.auth.sign_up(
            {
                'email': payload.email,
                'password': payload.password,
            }
        )

        return {
            'user': res.user.model_dump() if res.user else None,
            'session': res.session.model_dump() if res.session else None,
            'message': 'Signup successfully.',
        }
    except Exception as e:
        # Supabase throws AuthApiError
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/login', response_model=LoginResponse)
def login(payload: LoginRequest):
    sb = supabase_client_user()
    try:
        res = sb.auth.sign_in_with_password(
            {
                'email': payload.email,
                'password': payload.password,
            }
        )
        if not res.session or not res.session.access_token:
            raise HTTPException(status_code=401, detail='Login failed.')

        return {
            'access_token': res.session.access_token,
            'refresh_token': res.session.refresh_token,
            'user': res.user.model_dump() if res.user else {},
        }
    except Exception as e:
        # Wrong password / user not found / email not confirmed...
        raise HTTPException(status_code=401, detail=str(e))


@router.post('/refresh', response_model=RefreshResponse)
def refresh(payload: RefreshRequest):
    sb = supabase_client_user()
    try:
        res = sb.auth.refresh_session(payload.refresh_token)
        if not res.session or not res.session.access_token:
            raise HTTPException(status_code=401, detail='Invalid refresh token.')

        return {
            'access_token': res.session.access_token,
            'refresh_token': res.session.refresh_token,
            'user': res.user.model_dump() if res.user else {},
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
