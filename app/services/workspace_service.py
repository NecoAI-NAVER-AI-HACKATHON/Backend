from uuid import UUID
from fastapi import HTTPException, status

from app.models.workspace import Workspace
from app.repositories.workspace_repository import WorkspaceRepository
from app.schemas.workspace_schema import (
    CreateWorkspaceRequest,
    WorkspaceResponse,
    WorkspaceListResponse,
    SearchWorkspaceRequest,
)


class WorkspaceService:
    def __init__(self, workspace_repo: WorkspaceRepository):
        self._workspace_repo = workspace_repo

    def create_workspace(
        self, payload: CreateWorkspaceRequest, user_id: UUID
    ) -> WorkspaceResponse:
        try:
            workspace = Workspace(
                name=payload.name, description=payload.description, user_id=user_id
            )

            saved_workspace = self._workspace_repo.create(workspace)
            if not saved_workspace:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail='Create workspace failed.',
                )

            return WorkspaceResponse(**saved_workspace.model_dump())
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_workspace(self, workspace_id: UUID, user_id: UUID) -> WorkspaceResponse:
        try:
            found_workspace = self._workspace_repo.find_by_id(workspace_id)
            if not found_workspace:
                raise HTTPException(status_code=404, detail='Workspace not found.')

            if found_workspace.user_id != user_id:
                raise HTTPException(
                    status_code=403, detail='Not authorized to access this workspace.'
                )

            return WorkspaceResponse(**found_workspace.model_dump())
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_all_workspaces(
        self, user_id: UUID, page: int = 1, per_page: int = 10
    ) -> WorkspaceListResponse:
        try:
            if page < 1:
                raise HTTPException(status_code=400, detail='Page must be >= 1')
            if per_page < 1:
                raise HTTPException(status_code=400, detail='per_page must be >= 1')

            offset = (page - 1) * per_page

            workspaces, total = self._workspace_repo.find_all_by_user_id(
                user_id, offset=offset, limit=per_page
            )

            return WorkspaceListResponse(
                workspaces=workspaces, total=total, page=page, per_page=per_page
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def search_workspace(
        self, payload: SearchWorkspaceRequest, user_id: UUID
    ) -> WorkspaceListResponse:
        try:
            workspaces = self._workspace_repo.search_by_criteria(
                user_id,
                name=payload.name,
                status=payload.status,
                sorting=payload.sorting,
                order=payload.order,
            )

            return workspaces
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    # def update_workspace(
    #     self, workspace_id: uuid.UUID, payload: UpdateWorkspaceRequest
    # ) -> UpdateWorkspaceResponse:
    #     workspace = self._workspace_repo.get(workspace_id)
    #     if not workspace:
    #         raise HTTPException(status_code=404, detail='Workspace not found.')

    #     workspace.name = payload.name
    #     self._workspace_repo.update(workspace)
    #     return UpdateWorkspaceResponse(workspace=workspace.model_dump())

    def delete_workspace(self, workspace_id: UUID, user_id: UUID) -> dict:
        try:
            found_workspace = self._workspace_repo.find_by_id(workspace_id)
            if not found_workspace:
                raise HTTPException(status_code=404, detail='Workspace not found.')

            if found_workspace.user_id != user_id:
                raise HTTPException(
                    status_code=403, detail='Not authorized to delete this workspace.'
                )

            self._workspace_repo.delete(found_workspace.id)

            return {'message': 'Workspace deleted successfully.'}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
