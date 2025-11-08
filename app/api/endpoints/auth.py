from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials

from dependency_injector.wiring import Provide, inject

from app.core.containers.application_container import ApplicationContainer
from app.schemas.auth_schema import (
    LogoutResponse,
    SignupRequest,
    SignupResponse,
    LoginRequest,
    LoginResponse,
    RefreshRequest,
    RefreshResponse,
)
from app.services.auth_service import AuthService
from app.core.dependencies.auth_deps import bearer_scheme

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/signup', response_model=SignupResponse, status_code=status.HTTP_201_CREATED
)
@inject
def signup(
    payload: SignupRequest,
    auth_service: AuthService = Depends(
        Provide[ApplicationContainer.services.auth_service]
    ),
):
    try:
        return auth_service.sign_up(payload)
    except Exception as e:
        # Supabase throws AuthApiError
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/login', response_model=LoginResponse)
@inject
def login(
    payload: LoginRequest,
    auth_service: AuthService = Depends(
        Provide[ApplicationContainer.services.auth_service]
    ),
):
    try:
        return auth_service.login(payload)
    except Exception as e:
        # Wrong password / user not found / email not confirmed...
        raise HTTPException(status_code=401, detail=str(e))


@router.post('/refresh', response_model=RefreshResponse)
@inject
def refresh(
    payload: RefreshRequest,
    auth_service: AuthService = Depends(
        Provide[ApplicationContainer.services.auth_service]
    ),
):
    try:
        return auth_service.refresh(payload)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post('/logout', response_model=LogoutResponse)
@inject
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: AuthService = Depends(
        Provide[ApplicationContainer.services.auth_service]
    ),
):
    try:
        # Sign out the user using the provided JWT
        # This will revoke the refresh token and clear the session.
        token = credentials.credentials if credentials else None
        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='No token provided for logout.',
            )

        return auth_service.logout(token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
