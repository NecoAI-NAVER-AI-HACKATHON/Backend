from typing import Optional
from fastapi import Depends, HTTPException, status

from dependency_injector.wiring import inject, Provide

from app.core.containers.application_container import ApplicationContainer
from app.schemas.node_definition_schema import (
    FileUploadTriggerNode,
    NodeDefinitionResponse,
)
from app.services.node_definition_service import NodeDefinitionService


@inject
def get_trigger_config(
    node_def_svc: NodeDefinitionService = Depends(
        Provide[ApplicationContainer.services.node_definition_service]
    ),
) -> Optional[FileUploadTriggerNode]:
    try:
        upload_trigger_def = node_def_svc.get_node_definition(
            "40000000-0000-0000-0000-000000000002"
        )
        return upload_trigger_def
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving trigger configuration: {str(e)}",
        )
