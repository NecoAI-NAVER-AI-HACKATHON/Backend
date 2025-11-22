from uuid import UUID
from fastapi import HTTPException, status, BackgroundTasks

from app.core.dependencies.redis import WorkflowClient
from app.models.system_execution import SystemExecution
from app.repositories.system_execution_repository import SystemExecutionRepository
from app.repositories.system_repository import SystemRepository
from app.schemas.system_execution_schema import (
    CreateSystemExecutionRequest,
    SystemExecutionResponse,
)


async def trigger_workflow_in_background(
    execution: SystemExecutionResponse,
    workflow_client=WorkflowClient,
) -> bool:
    print("Starting workflow in background task...")
    try:
        await workflow_client.connect()
        workflow_client.load_workflow(execution.system_json)
        # run one-off trigger
        await workflow_client.trigger_node_manual()
        # close redis
        await workflow_client.close()
        return True
    except Exception as e:
        print(f"Error triggering workflow: {e}")
        return False


class SystemExecutionService:
    def __init__(
        self,
        execution_repo: SystemExecutionRepository,
        system_repo: SystemRepository,
        workflow_client=WorkflowClient,
    ):
        self._execution_repo = execution_repo
        self._system_repo = system_repo
        self._workflow_client = workflow_client

    def create_execution(
        self, payload: CreateSystemExecutionRequest
    ) -> SystemExecutionResponse:
        try:
            # validate referenced system exists
            found_system = self._system_repo.find_by_id(payload.system_id)
            if not found_system:
                raise HTTPException(status_code=404, detail='System not found.')

            execution = SystemExecution(
                system_id=payload.system_id,
                system_json=payload.system_json,
                logs=None,
                status=payload.status,
                started_at=None,
                stopped_at=None,
            )

            saved = self._execution_repo.create(execution)
            if not saved:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail='Create execution failed.',
                )

            return SystemExecutionResponse(**saved.model_dump())
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_execution(self, execution_id: UUID) -> SystemExecutionResponse:
        try:
            found = self._execution_repo.find_by_id(execution_id)
            if not found:
                raise HTTPException(status_code=404, detail='Execution not found.')

            return SystemExecutionResponse(**found.model_dump())
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def start(
        self, execution_id: UUID, background_tasks: BackgroundTasks
    ) -> dict:
        try:
            execution = self._execution_repo.find_by_id(execution_id)
            if not execution:
                raise HTTPException(status_code=404, detail='Execution not found.')

            if execution.status == 'running':
                raise HTTPException(
                    status_code=400, detail='Execution is already running.'
                )

            # Update status to 'running'
            execution.status = 'running'
            self._execution_repo.update(execution.id, execution)

            # `model_dump()` returns a dict; `model_validate` expects the data
            # as a single positional argument in pydantic v2, not keyword args.
            execution = SystemExecutionResponse(**execution.model_dump())

            background_tasks.add_task(
                trigger_workflow_in_background,
                execution,
                self._workflow_client,
            )

            return {"message": "Execution started."}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
