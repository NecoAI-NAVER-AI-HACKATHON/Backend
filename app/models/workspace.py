from uuid import UUID
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, func, Index
from app.models.base_model import BaseModel


class Workspace(BaseModel, table=True):
    __table_args__ = (Index('ix_workspace', 'id', unique=True),)

    name: str = Field(nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    status: str = Field(default='activate')
    systems_count: int = Field(default=0)
    user_id: UUID = Field(foreign_key='users.id')

    created_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=None, onupdate=func.now()),
    )
