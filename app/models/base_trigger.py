from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, func


class BaseTriggerNode(BaseModel):
    id: str
    name: str
    outputSchema: Optional[dict] = Field(
        default_factory=dict, sa_column=Column(JSON, nullable=True)
    )


class BaseNodeDefinition(BaseModel):
    name: str = Field(nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    is_public: bool = Field(default=False)
    input_type: Optional[str] = Field(default=None, nullable=True)
    output_type: Optional[str] = Field(default=None, nullable=True)
    outputSchema: Optional[dict] = Field(
        default_factory=dict, sa_column=Column(JSON, nullable=True)
    )
    created_by: UUID = Field(foreign_key='users.id')
    created_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=None, onupdate=func.now()),
    )
