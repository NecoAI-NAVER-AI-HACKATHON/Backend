from fastapi import APIRouter, HTTPException, Depends

from dependency_injector.wiring import Provide, inject

from app.core.containers.application_container import ApplicationContainer
from app.db.database import Database
from app.api.endpoints.auth import oauth2_scheme

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/me', response_model=dict)
@inject
def get_current_user(
    db: Database = Depends(Provide[ApplicationContainer.database.db]),
    token: str = Depends(oauth2_scheme),
):
    try:
        sb = db.get_client()
        user = sb.auth.get_user(token)
        if not user or not user.user:
            raise HTTPException(status_code=401, detail='Invalid token.')

        return user.user.model_dump()
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
