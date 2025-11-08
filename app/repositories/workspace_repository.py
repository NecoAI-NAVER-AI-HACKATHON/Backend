from uuid import UUID
from contextlib import AbstractContextManager
from typing import Callable

from sqlmodel import Session

from app.models.workspace import Workspace
from app.repositories.base_repository import BaseRepository
from app.schemas.workspace_schema import WorkspaceResponse


class WorkspaceRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, Workspace)

    def find_all_by_user_id(self, user_id: UUID) -> list[WorkspaceResponse]:
        with self.session_factory() as session:
            workspaces = (
                session.query(Workspace).filter(Workspace.user_id == user_id).all()
            )
            if not workspaces:
                return []

            return [WorkspaceResponse.model_validate(ws) for ws in workspaces]
