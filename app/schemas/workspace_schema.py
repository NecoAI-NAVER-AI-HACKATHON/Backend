from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.base_schema import ModelBaseInfo


class BaseWorkspace(BaseModel):
    name: str
    description: str | None
    status: str
    systems_count: int
    user_id: UUID

    # Pydantic configuration to work with ORM models
    # It means we can create Pydantic models from ORM objects directly
    class Config:
        from_attributes = True


class CreateWorkspaceRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1024)


class WorkspaceResponse(ModelBaseInfo, BaseWorkspace): ...


class WorkspaceListResponse(BaseModel):
    workspaces: list[WorkspaceResponse]
    total: int
