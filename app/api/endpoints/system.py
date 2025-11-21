import json
from uuid import UUID, uuid4
from fastapi import APIRouter, HTTPException, Depends, Request, status

from dependency_injector.wiring import Provide, inject

from app.core.containers.application_container import ApplicationContainer
from app.core.dependencies.auth_deps import get_current_user
from app.schemas.system_schema import (
    CreateSystemRequest,
    SystemListResponse,
    SystemResponse,
)
from app.schemas.user_schema import UserResponse
from app.services.system_service import SystemService

router = APIRouter(prefix='/workspaces', tags=['system info'])


@router.post(
    '/system', response_model=SystemResponse, status_code=status.HTTP_201_CREATED
)
@inject
def create_system(
    payload: CreateSystemRequest,
    current_user: UserResponse = Depends(get_current_user),
    system_service: SystemService = Depends(
        Provide[ApplicationContainer.services.system_service]
    ),
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail='Unauthorized access.')

        return system_service.create_system(payload, current_user.id)
    except Exception:
        raise


@router.get('/{workspace_id}/systems', response_model=SystemListResponse)
@inject
def get_systems(
    workspace_id: str,
    current_user: UserResponse = Depends(get_current_user),
    system_service: SystemService = Depends(
        Provide[ApplicationContainer.services.system_service]
    ),
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail='Unauthorized access.')

        return system_service.get_all_systems(UUID(workspace_id), current_user.id)
    except Exception:
        raise


@router.get('/{workspace_id}/systems/{system_id}', response_model=SystemResponse)
@inject
def get_system_info(
    workspace_id: str,
    system_id: str,
    current_user: UserResponse = Depends(get_current_user),
    system_service: SystemService = Depends(
        Provide[ApplicationContainer.services.system_service]
    ),
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail='Unauthorized access.')

        return system_service.get_system(
            UUID(workspace_id), UUID(system_id), current_user.id
        )
    except Exception:
        raise


@router.post('/{workspace_id}/systems/{system_id}/activate', response_model=dict)
@inject
async def activate_system(
    request: Request,
    workspace_id: str,
    system_id: str,
    # current_user: UserResponse = Depends(get_current_user),
    system_service: SystemService = Depends(
        Provide[ApplicationContainer.services.system_service]
    ),
):
    try:
        # if not current_user:
        #     raise HTTPException(status_code=401, detail='Unauthorized access.')

        # Check hard-code: workspace_id must be "1"
        if workspace_id != "1":
            raise HTTPException(
                status_code=403, detail='Activation allowed only in workspace 1.'
            )
        # Check hard-code: system_id must be "1"
        if system_id != "1":
            raise HTTPException(
                status_code=403, detail='Activation allowed only for system 1.'
            )
        # Read workflow from workflow.json
        workflow_file = 'workflow.json'
        try:
            with open(workflow_file, 'r') as f:
                workflow_data = f.read()
                # Calculate the size of the workflow file
                file_size = len(workflow_data)
                print(f"Activating system with workflow file size: {file_size} bytes")
                # Parse to json
                req = json.loads(workflow_data)
                # enqueue initial job
                job = {
                    "job_id": str(uuid4()),
                    "workflow_id": req["id"],
                    "task_name": "start",
                    "payload": req,
                    "exec_id": str(uuid4()),
                }
                print(f"Enqueued job: {job['job_id']}")
                await request.app.state.redis.lpush("queue:main", json.dumps(job))
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail='Workflow file not found.')

        return {"message": "System activated successfully."}
    except Exception:
        raise
