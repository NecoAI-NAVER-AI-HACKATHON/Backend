from uuid import UUID
from contextlib import AbstractContextManager
from typing import Callable

from sqlmodel import Session

from app.models.system_execution import SystemExecution
from app.repositories.base_repository import BaseRepository
from app.schemas.system_execution_schema import SystemExecutionResponse


class SystemExecutionRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, SystemExecution)

    def find_all_by_system_id(self, system_id: UUID) -> list[SystemExecutionResponse]:
        with self.session_factory() as session:
            executions = (
                session.query(SystemExecution)
                .filter(SystemExecution.system_id == system_id)
                .all()
            )
            if not executions:
                return []

            return [
                SystemExecutionResponse.model_validate(exec_) for exec_ in executions
            ]
