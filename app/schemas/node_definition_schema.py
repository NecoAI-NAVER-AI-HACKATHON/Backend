from uuid import UUID
from typing import Literal, List

from pydantic import BaseModel

from app.schemas.base_schema import ModelBaseInfo


class BaseNodeDefinition(BaseModel):
    name: str
    description: str | None
    is_public: bool
    input_type: str | None
    output_type: str | None
    created_by: UUID

    # Pydantic configuration to work with ORM models
    # It means we can create Pydantic models from ORM objects directly
    class Config:
        from_attributes = True


class FileUploadTriggerParameters(BaseModel):
    acceptedFileTypes: List[str]
    maxSizeMB: int


class FileUploadTriggeroOutputSchema(BaseModel):
    filePath: str
    fileName: str
    fileType: str


class FileUploadTriggerNode(ModelBaseInfo, BaseNodeDefinition):
    type: Literal["trigger"]
    parameters: FileUploadTriggerParameters
    output_schema: FileUploadTriggeroOutputSchema


class NodeDefinitionResponse(ModelBaseInfo, BaseNodeDefinition): ...


class NodeDefinitionListResponse(BaseModel):
    node_definitions: list[NodeDefinitionResponse]
    total: int
