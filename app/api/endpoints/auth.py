# app/api/endpoints/auth.py
from fastapi import APIRouter, HTTPException, status, Response
from supabase import create_client, Client
from app.core.config import configs
from app.utils.auth_cookies import set_auth_cookies, clear_auth_cookies
from app.schemas.auth_schema import (
    SignupRequest, SignupResponse, LoginRequest, LoginResponse,
    RefreshRequest, RefreshResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])

def supabase_client_user() -> Client:
    return create_client(configs.SUPABASE_URL, configs.SUPABASE_ANON_KEY)

@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, response: Response):
    sb = supabase_client_user()
    try:
        res = sb.auth.sign_up({"email": payload.email, "password": payload.password})
        if res.session and res.session.access_token:
            set_auth_cookies(response, res.session.access_token, res.session.refresh_token)
        return {
            "user": res.user.model_dump() if res.user else None,
            "session": res.session.model_dump() if res.session else None,
            "message": "Signup successfully.",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, response: Response):
    sb = supabase_client_user()
    try:
        res = sb.auth.sign_in_with_password({"email": payload.email, "password": payload.password})
        if not res.session or not res.session.access_token:
            raise HTTPException(status_code=401, detail="Login failed.")
        set_auth_cookies(response, res.session.access_token, res.session.refresh_token)
        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "user": res.user.model_dump() if res.user else {},
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/refresh", response_model=RefreshResponse)
def refresh(payload: RefreshRequest, response: Response):
    sb = supabase_client_user()
    try:
        res = sb.auth.refresh_session(payload.refresh_token)
        if not res.session or not res.session.access_token:
            raise HTTPException(status_code=401, detail="Invalid refresh token.")
        set_auth_cookies(response, res.session.access_token, res.session.refresh_token)
        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "user": res.user.model_dump() if res.user else {},
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout")
def logout(response: Response):
    clear_auth_cookies(response)
    return {"message": "Logged out"}
