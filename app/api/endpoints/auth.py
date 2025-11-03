from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from dependency_injector.wiring import Provide, inject

from app.core.containers.application_container import ApplicationContainer
from app.db.database import Database
from app.schemas.auth_schema import (
    LogoutResponse,
    SignupRequest,
    SignupResponse,
    LoginRequest,
    LoginResponse,
    RefreshRequest,
    RefreshResponse,
)

router = APIRouter(prefix='/auth', tags=['auth'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


@router.post(
    '/signup', response_model=SignupResponse, status_code=status.HTTP_201_CREATED
)
@inject
def signup(
    payload: SignupRequest,
    db: Database = Depends(Provide[ApplicationContainer.database.db]),
):
    try:
        sb = db.get_client()
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
@inject
def login(
    payload: LoginRequest,
    db: Database = Depends(Provide[ApplicationContainer.database.db]),
):
    try:
        sb = db.get_client()
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
@inject
def refresh(
    payload: RefreshRequest,
    db: Database = Depends(Provide[ApplicationContainer.database.db]),
):
    try:
        sb = db.get_client()
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


@router.post('/logout', response_model=LogoutResponse)
@inject
def logout(
    token: str = Depends(oauth2_scheme),
    db: Database = Depends(Provide[ApplicationContainer.database.db]),
):
    try:
        # Sign out the user using the provided JWT
        # This will revoke the refresh token and clear the session.
        sb = db.get_client()
        sb.auth.admin.sign_out(token)

        return {
            'message': 'Logout successfully.',
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
