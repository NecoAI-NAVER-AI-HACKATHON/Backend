from typing import Optional
from pydantic import BaseModel, EmailStr

from app.schemas.base_schema import ModelBaseInfo


class BaseUser(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    role: Optional[str] = None

    class Config:
        from_attributes = True


class UserResponse(ModelBaseInfo, BaseUser):
    pass
