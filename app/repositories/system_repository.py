from contextlib import AbstractContextManager
from typing import Callable

from sqlmodel import Session

from app.models.system import System
from app.repositories.base_repository import BaseRepository
from app.schemas.system_schema import SystemResponse


class SystemRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, System)

    def find_all_by_workspace_id(self, workspace_id: str) -> list[SystemResponse]:
        with self.session_factory() as session:
            systems = (
                session.query(System).filter(System.workspace_id == workspace_id).all()
            )
            if not systems:
                return []

            return [SystemResponse.model_validate(sys) for sys in systems]
