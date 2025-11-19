from uuid import UUID
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, func, JSON
from app.models.base_model import BaseModel


class NodeDefinition(BaseModel, table=True):
    __tablename__ = "node_definitions"

    name: str = Field(nullable=False)
    type: str = Field(nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    parameters: Optional[dict] = Field(
        default_factory=dict, sa_column=Column(JSON, nullable=True)
    )
    is_public: bool = Field(default=False)
    input_schema: Optional[str] = Field(default=None, nullable=True)
    output_schema: Optional[dict] = Field(
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
