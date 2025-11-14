from uuid import UUID
from contextlib import AbstractContextManager
from typing import Callable

from sqlmodel import Session

from app.models.workspace import Workspace
from app.repositories.base_repository import BaseRepository
from app.schemas.workspace_schema import WorkspaceListResponse, WorkspaceResponse


class WorkspaceRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, Workspace)

    def find_all_by_user_id(
        self, user_id: UUID, offset: int = 0, limit: int | None = None
    ) -> tuple[list[WorkspaceResponse], int]:
        """Return a tuple (workspaces, total) for the given user.

        Args:
                        user_id: id of the user who owns the workspaces
                        offset: number of items to skip
                        limit: maximum number of items to return (None means no limit)

        Returns:
                        (list[WorkspaceResponse], total_count)
        """
        with self.session_factory() as session:
            base_query = session.query(Workspace).filter(Workspace.user_id == user_id)

            total = base_query.count()

            query = base_query.offset(offset)
            if limit is not None:
                query = query.limit(limit)

            workspaces = query.all()

            if not workspaces:
                return [], total

            return [WorkspaceResponse.model_validate(ws) for ws in workspaces], total

    def search_by_criteria(
        self,
        user_id: UUID,
        name: str | None = None,
        status: str | None = None,
        sorting: str | None = None,
        order: str | None = None,
        offset: int = 0,
        limit: int | None = None,
    ) -> WorkspaceListResponse:
        """Search workspaces by criteria for the given user.

        Args:
                        user_id: id of the user who owns the workspaces
                        name: name filter (partial match)
                        status: status filter (exact match)
                        sorting: field to sort by (e.g., 'name', 'created_at')
                        order: 'asc' or 'desc'
                        offset: number of items to skip
                        limit: maximum number of items to return (None means no limit)

        Returns:
                        (list[WorkspaceResponse], total_count)
        """
        with self.session_factory() as session:
            base_query = session.query(Workspace).filter(Workspace.user_id == user_id)

            if name:
                base_query = base_query.filter(Workspace.name.ilike(f"%{name}%"))
            if status:
                base_query = base_query.filter(Workspace.status == status)

            total = base_query.count()

            if sorting:
                sort_column = getattr(Workspace, sorting, None)
                if sort_column is not None:
                    if order == 'desc':
                        sort_column = sort_column.desc()
                    else:
                        sort_column = sort_column.asc()
                    base_query = base_query.order_by(sort_column)

            query = base_query.offset(offset)
            if limit is not None:
                query = query.limit(limit)

            workspaces = query.all()

            if not workspaces:
                return WorkspaceListResponse(workspaces=[], total=total)

            return WorkspaceListResponse(
                workspaces=[WorkspaceResponse.model_validate(ws) for ws in workspaces],
                total=total,
            )
