from uuid import UUID
from typing import Optional
from datetime import datetime

from sqlmodel import Field, SQLModel, Column, JSON, DateTime, func, Index

from app.models.base_model import BaseModel


class SystemExecution(BaseModel, table=True):
    __tablename__ = 'system_execution'
    __table_args__ = (Index('ix_system_execution', 'id', unique=True),)

    system_id: UUID = Field(foreign_key='systems.id')

    system_json: Optional[dict] = Field(
        default_factory=dict,
        sa_column=Column(JSON, nullable=True),
        description='System configuration in JSON format',
    )

    logs: Optional[dict] = Field(
        default_factory=dict,
        sa_column=Column(JSON, nullable=True),
        description='Execution logs in JSON format',
    )

    status: Optional[str] = Field(
        default='', nullable=True, description='Current status of the execution'
    )

    started_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=None),
    )

    stopped_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=None),
    )
