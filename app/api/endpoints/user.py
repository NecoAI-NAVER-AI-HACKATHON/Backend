from fastapi import APIRouter, HTTPException, Depends

from app.core.dependencies.auth_deps import get_current_user

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/me', response_model=dict)
def get_user_profile(
    current_user=Depends(get_current_user),
):
    try:
        return current_user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
