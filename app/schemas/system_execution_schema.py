from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.base_schema import ModelBaseInfo


class CreateSystemExecutionRequest(BaseModel):
    system_id: UUID = Field(...)
    system_json: Optional[dict] = Field(default_factory=dict)
    status: Optional[str] = Field(default='active')


class SystemExecutionResponse(ModelBaseInfo):
    system_id: UUID
    system_json: Optional[dict] = Field(default_factory=dict)
    logs: Optional[list[dict]] = Field(default_factory=list)
    status: Optional[str] = ''
    started_at: Optional[datetime] = None
    stopped_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SystemExecutionListResponse(BaseModel):
    executions: list[SystemExecutionResponse]
    total: int
