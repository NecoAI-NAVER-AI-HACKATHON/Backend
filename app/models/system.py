from uuid import UUID
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, func, Index, JSON
from app.models.base_model import BaseModel


class System(BaseModel, table=True):
    __tablename__ = 'systems'
    __table_args__ = (Index('ix_system', 'id', unique=True),)

    name: str = Field(unique=True)
    description: Optional[str] = Field(default=None, nullable=True)
    status: str = Field(default='activate')
    # use Optional and default_factory to avoid mutable defaults and allow
    # existing DB rows with NULL values. We'll coerce None -> {} at the
    # repository layer when returning models to the API.
    global_config: Optional[dict] = Field(
        default_factory=dict, sa_column=Column(JSON, nullable=True)
    )
    # change column name to avoid conflict with reserved word 'metadata'
    # but keep the database column name as 'metadata'
    metadata_info: Optional[dict] = Field(
        default_factory=dict, sa_column=Column('metadata', JSON, nullable=True)
    )
    workspace_id: UUID = Field(foreign_key='workspace.id')

    created_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=None, onupdate=func.now()),
    )
