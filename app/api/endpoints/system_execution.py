from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends, status

from dependency_injector.wiring import Provide, inject

from app.core.containers.application_container import ApplicationContainer
from app.core.dependencies.auth_deps import get_current_user
from app.schemas.user_schema import UserResponse
from app.schemas.system_execution_schema import (
    CreateSystemExecutionRequest,
    SystemExecutionResponse,
)
from app.services.system_execution_service import SystemExecutionService


router = APIRouter(prefix='/executions', tags=['system execution'])


@router.post(
    '/', response_model=SystemExecutionResponse, status_code=status.HTTP_201_CREATED
)
@inject
def create_execution(
    payload: CreateSystemExecutionRequest,
    current_user: UserResponse = Depends(get_current_user),
    execution_service: SystemExecutionService = Depends(
        Provide[ApplicationContainer.services.system_execution_service]
    ),
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail='Unauthorized access.')

        return execution_service.create_execution(payload)
    except Exception:
        raise


@router.get('/{execution_id}', response_model=SystemExecutionResponse)
@inject
def get_execution(
    execution_id: str,
    current_user: UserResponse = Depends(get_current_user),
    execution_service: SystemExecutionService = Depends(
        Provide[ApplicationContainer.services.system_execution_service]
    ),
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail='Unauthorized access.')

        return execution_service.get_execution(UUID(execution_id))
    except Exception:
        raise


@router.post('/{execution_id}', response_model=dict)
@inject
async def start_workflow(
    execution_id: str,
    # current_user: UserResponse = Depends(get_current_user),
    background_tasks: BackgroundTasks,
    execution_service: SystemExecutionService = Depends(
        Provide[ApplicationContainer.services.system_execution_service]
    ),
):
    try:
        # if not current_user:
        #     raise HTTPException(status_code=401, detail='Unauthorized access.')

        return await execution_service.start(UUID(execution_id), background_tasks)
    except Exception:
        raise
