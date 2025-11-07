from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, func, Index
from app.models.base_model import BaseModel


class User(BaseModel, table=True):
    __tablename__ = 'users'

    email: str = Field(unique=True)
    username: Optional[str] = Field(default=None, nullable=True)
    role: str = Field(default='user')
    avatar_url: Optional[str] = Field(default=None, nullable=True)

    created_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), default=func.now(), onupdate=func.now()
        ),
    )
