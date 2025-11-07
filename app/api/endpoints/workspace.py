from fastapi import APIRouter, HTTPException, Depends

from dependency_injector.wiring import Provide, inject

from app.core.containers.application_container import ApplicationContainer
from app.core.dependencies.auth_deps import get_current_user
from app.schemas.user_schema import UserResponse
from app.schemas.workspace_schema import (
    CreateWorkspaceRequest,
    WorkspaceListResponse,
    WorkspaceResponse,
)
from app.services.workspace_service import WorkspaceService

router = APIRouter(prefix='/workspace', tags=['workspace'])


@router.post('/', response_model=WorkspaceResponse)
@inject
def create_workspace(
    payload: CreateWorkspaceRequest,
    current_user: UserResponse = Depends(get_current_user),
    workspace_service: WorkspaceService = Depends(
        Provide[ApplicationContainer.services.workspace_service]
    ),
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized access.")

        return workspace_service.create_workspace(payload, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get('/', response_model=WorkspaceListResponse)
@inject
def get_workspace(
    current_user: UserResponse = Depends(get_current_user),
    workspace_service: WorkspaceService = Depends(
        Provide[ApplicationContainer.services.workspace_service]
    ),
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized access.")

        return workspace_service.get_all_workspaces(current_user.id)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get('/{workspace_id}', response_model=WorkspaceResponse)
@inject
def get_workspace_info(
    workspace_id: str,
    current_user: UserResponse = Depends(get_current_user),
    workspace_service: WorkspaceService = Depends(
        Provide[ApplicationContainer.services.workspace_service]
    ),
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized access.")
        if not workspace_id:
            raise HTTPException(status_code=400, detail="Workspace ID is required.")

        return workspace_service.get_workspace(workspace_id, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.delete('/{workspace_id}', response_model=dict)
@inject
def delete_workspace(
    workspace_id: str,
    current_user: UserResponse = Depends(get_current_user),
    workspace_service: WorkspaceService = Depends(
        Provide[ApplicationContainer.services.workspace_service]
    ),
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized access.")
        if not workspace_id:
            raise HTTPException(status_code=400, detail="Workspace ID is required.")

        return workspace_service.delete_workspace(workspace_id)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
