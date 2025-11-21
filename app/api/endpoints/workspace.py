from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends, status

from dependency_injector.wiring import Provide, inject

from app.core.containers.application_container import ApplicationContainer
from app.core.dependencies.auth_deps import get_current_user
from app.schemas.user_schema import UserResponse
from app.schemas.workspace_schema import (
    CreateWorkspaceRequest,
    WorkspaceListResponse,
    WorkspaceResponse,
    SearchWorkspaceRequest,
)
from app.services.workspace_service import WorkspaceService

router = APIRouter(prefix='/workspaces', tags=['workspace'])


@router.post('/', response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
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
            raise HTTPException(status_code=401, detail='Unauthorized access.')

        return workspace_service.create_workspace(payload, current_user.id)
    except Exception:
        raise


@router.get('/', response_model=WorkspaceListResponse)
@inject
def get_workspace(
    page: int = 1,
    per_page: int = 10,
    current_user: UserResponse = Depends(get_current_user),
    workspace_service: WorkspaceService = Depends(
        Provide[ApplicationContainer.services.workspace_service]
    ),
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail='Unauthorized access.')

        return workspace_service.get_all_workspaces(current_user.id, page, per_page)
    except Exception:
        raise


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
            raise HTTPException(status_code=401, detail='Unauthorized access.')

        return workspace_service.get_workspace(UUID(workspace_id), current_user.id)
    except Exception:
        raise


@router.post('/search', response_model=WorkspaceListResponse)
@inject
def search_workspace(
    payload: SearchWorkspaceRequest,
    current_user: UserResponse = Depends(get_current_user),
    workspace_service: WorkspaceService = Depends(
        Provide[ApplicationContainer.services.workspace_service]
    ),
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail='Unauthorized access.')

        return workspace_service.search_workspace(payload, current_user.id)
    except Exception:
        raise


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
            raise HTTPException(status_code=401, detail='Unauthorized access.')

        return workspace_service.delete_workspace(UUID(workspace_id), current_user.id)
    except Exception:
        raise
