from uuid import UUID
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, func, Index, JSON
from app.models.base_model import BaseModel


class System(BaseModel, table=True):
    __tablename__ = 'systems'
    __table_args__ = (Index('ix_system', 'id', unique=True),)

    name: str = Field(nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    nodes_count: Optional[int] = Field(default=0, nullable=True)
    workspace_id: UUID = Field(foreign_key='workspace.id')

    created_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=None, onupdate=func.now()),
    )
