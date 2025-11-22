from pydantic import BaseModel, Field
from typing import List, Literal

from app.models.base_trigger import BaseNodeDefinition


class FileUploadTriggerParameters(BaseModel):
    acceptedFileTypes: List[str] = Field(default_factory=list)
    maxSizeMB: int = 50
    storageType: Literal["local", "cloud"] = "local"


class FileUploadTriggerNode(BaseNodeDefinition):
    type: Literal["trigger"]
    subtype: Literal["file_upload"]
    parameters: FileUploadTriggerParameters
