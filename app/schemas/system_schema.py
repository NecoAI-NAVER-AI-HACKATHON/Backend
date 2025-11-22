from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.base_schema import ModelBaseInfo


class BaseSystem(BaseModel):
    name: str
    description: str | None
    nodes_count: int
    workspace_id: UUID

    # Pydantic configuration to work with ORM models
    # It means we can create Pydantic models from ORM objects directly
    class Config:
        from_attributes = True


class CreateSystemRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1024)
    workspace_id: UUID


class SystemResponse(ModelBaseInfo, BaseSystem): ...


class SystemListResponse(BaseModel):
    systems: list[SystemResponse]
    total: int
