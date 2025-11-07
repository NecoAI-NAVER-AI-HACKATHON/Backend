from uuid import UUID
from fastapi import HTTPException, status

from app.models.user import User
from app.models.workspace import Workspace
from app.repositories.workspace_repository import WorkspaceRepository
from app.schemas.workspace_schema import (
    CreateWorkspaceRequest,
    WorkspaceResponse,
    WorkspaceListResponse,
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
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_all_workspaces(self, user_id: UUID) -> WorkspaceListResponse:
        try:
            workspaces = self._workspace_repo.find_all_by_user_id(user_id)

            return WorkspaceListResponse(workspaces=workspaces, total=len(workspaces))
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

    def delete_workspace(self, workspace_id: UUID) -> dict:
        try:
            found_workspace = self._workspace_repo.find_by_id(workspace_id)
            if not found_workspace:
                raise HTTPException(status_code=404, detail='Workspace not found.')

            self._workspace_repo.delete(found_workspace.id)

            return {"message": "Workspace deleted successfully."}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
