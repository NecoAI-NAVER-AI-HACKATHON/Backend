from uuid import UUID
from fastapi import HTTPException
from supabase_auth import Optional

from app.repositories.node_definition_repository import NodeDefinitionRepository
from app.schemas.node_definition_schema import (
    FileUploadTriggerNode,
    NodeDefinitionResponse,
)


class NodeDefinitionService:
    def __init__(self, node_definition_repo: NodeDefinitionRepository):
        self._node_definition_repo = node_definition_repo
        self._cache: Optional[FileUploadTriggerNode] = None

    def get_node_definition(self, node_definition_id: UUID) -> FileUploadTriggerNode:
        try:
            if self._cache:
                print("Returning cached NodeDefinition with ID:", node_definition_id)
                return self._cache

            print("Querying database for NodeDefinition with ID:", node_definition_id)
            found_node_definition = self._node_definition_repo.find_by_id(
                node_definition_id
            )
            if not found_node_definition:
                raise HTTPException(status_code=404, detail='NodeDefinition not found.')

            self._cache = FileUploadTriggerNode(**found_node_definition.model_dump())
            return self._cache
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
