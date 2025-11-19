from uuid import UUID
from fastapi import HTTPException, status

from app.models.system_execution import SystemExecution
from app.repositories.system_execution_repository import SystemExecutionRepository
from app.repositories.system_repository import SystemRepository
from app.schemas.system_execution_schema import (
    CreateSystemExecutionRequest,
    SystemExecutionResponse,
    SystemExecutionListResponse,
)


class SystemExecutionService:
    def __init__(
        self,
        execution_repo: SystemExecutionRepository,
        system_repo: SystemRepository,
    ):
        self._execution_repo = execution_repo
        self._system_repo = system_repo

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

    def get_executions_by_system(self, system_id: UUID) -> SystemExecutionListResponse:
        try:
            executions = self._execution_repo.find_all_by_system_id(system_id)
            return SystemExecutionListResponse(
                executions=executions, total=len(executions)
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
