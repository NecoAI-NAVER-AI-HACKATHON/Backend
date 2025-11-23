from uuid import UUID
from fastapi import HTTPException, status

from app.models.system import System
from app.repositories.system_repository import SystemRepository
from app.repositories.workspace_repository import WorkspaceRepository
from app.schemas.system_schema import (
    CreateSystemRequest,
    SystemResponse,
    SystemListResponse,
)


class SystemService:
    def __init__(
        self, system_repo: SystemRepository, workspace_repo: WorkspaceRepository
    ):
        self._system_repo = system_repo
        self._workspace_repo = workspace_repo

    def create_system(
        self, payload: CreateSystemRequest, user_id: UUID
    ) -> SystemResponse:
        try:
            found_workspace = self._workspace_repo.find_by_id(payload.workspace_id)
            if not found_workspace:
                raise HTTPException(status_code=404, detail='Workspace not found.')

            if found_workspace.user_id != user_id:
                raise HTTPException(
                    status_code=403, detail='Not authorized to access this workspace.'
                )

            system = System(
                name=payload.name,
                description=payload.description,
                workspace_id=found_workspace.id,
            )

            saved_system = self._system_repo.create(system)
            if not saved_system:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail='Create system failed.',
                )

            return SystemResponse(**saved_system.model_dump())
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_system(
        self, workspace_id: UUID, system_id: UUID, user_id: UUID
    ) -> SystemResponse:
        try:
            found_workspace = self._workspace_repo.find_by_id(workspace_id)
            if not found_workspace:
                raise HTTPException(status_code=404, detail='Workspace not found.')

            if found_workspace.user_id != user_id:
                raise HTTPException(
                    status_code=403, detail='Not authorized to access this workspace.'
                )

            found_system = self._system_repo.find_by_id(system_id)
            if not found_system:
                raise HTTPException(status_code=404, detail='System not found.')

            if found_system.workspace_id != found_workspace.id:
                raise HTTPException(
                    status_code=404, detail='System not found in this workspace.'
                )

            return SystemResponse(**found_system.model_dump())
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_all_systems(self, workspace_id: UUID, user_id: UUID) -> SystemListResponse:
        try:
            found_workspace = self._workspace_repo.find_by_id(workspace_id)
            if not found_workspace:
                raise HTTPException(status_code=404, detail='Workspace not found.')

            if found_workspace.user_id != user_id:
                raise HTTPException(
                    status_code=403, detail='Not authorized to access this workspace.'
                )

            systems = self._system_repo.find_all_by_workspace_id(workspace_id)

            return SystemListResponse(systems=systems, total=len(systems))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    # def update_system(
    #     self, system_id: uuid.UUID, payload: UpdateSystemRequest
    # ) -> UpdateSystemResponse:
    #     system = self._system_repo.get(system_id)
    #     if not system:
    #         raise HTTPException(status_code=404, detail='System not found.')

    #     system.name = payload.name
    #     self._system_repo.update(system)
    #     return UpdateSystemResponse(system=system.model_dump())

    # def delete_system(self, system_id: UUID, user_id: UUID) -> dict:
    #     try:
    #         found_system = self._system_repo.find_by_id(system_id)
    #         if not found_system:
    #             raise HTTPException(status_code=404, detail='System not found.')

    #         self._system_repo.delete(found_system.id)

    #         return {'message': 'System deleted successfully.'}
    #     except HTTPException:
    #         raise
    #     except Exception as e:
    #         raise HTTPException(status_code=400, detail=str(e))
