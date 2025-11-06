from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    role: str | None = None


class SignupResponse(BaseModel):
    user: dict
    session: dict | None
    message: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
    user: dict


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
    user: dict


class LogoutResponse(BaseModel):
    message: str
