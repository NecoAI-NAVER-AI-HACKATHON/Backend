from fastapi import APIRouter, HTTPException, Depends

from dependency_injector.wiring import Provide, inject

from app.core.containers.application_container import ApplicationContainer
from app.core.dependencies.auth_deps import get_current_user
from app.schemas.system_schema import (
    CreateSystemRequest,
    SystemListResponse,
    SystemResponse,
)
from app.services.system_service import SystemService

router = APIRouter(prefix='/workspace', tags=['system info'])


@router.post('/system', response_model=SystemResponse)
@inject
def create_system(
    payload: CreateSystemRequest,
    current_user=Depends(get_current_user),
    system_service: SystemService = Depends(
        Provide[ApplicationContainer.services.system_service]
    ),
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized access.")

        return system_service.create_system(payload, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get('/{workspace_id}/systems', response_model=SystemListResponse)
@inject
def get_systems(
    workspace_id: str,
    current_user=Depends(get_current_user),
    system_service: SystemService = Depends(
        Provide[ApplicationContainer.services.system_service]
    ),
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized access.")
        if not workspace_id:
            raise HTTPException(status_code=400, detail="Workspace ID is required.")

        return system_service.get_all_systems(workspace_id, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get('/{workspace_id}/systems/{system_id}', response_model=SystemResponse)
@inject
def get_system_info(
    workspace_id: str,
    system_id: str,
    current_user=Depends(get_current_user),
    system_service: SystemService = Depends(
        Provide[ApplicationContainer.services.system_service]
    ),
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized access.")
        if not workspace_id:
            raise HTTPException(status_code=400, detail="Workspace ID is required.")
        if not system_id:
            raise HTTPException(status_code=400, detail="System ID is required.")

        return system_service.get_system(workspace_id, system_id, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
