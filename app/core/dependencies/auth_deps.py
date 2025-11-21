from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from dependency_injector.wiring import inject, Provide

from app.core.containers.application_container import ApplicationContainer
from app.db.databases.supabase import SupabaseDatabase
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserResponse

# auto_error=False to allow optional authentication
bearer_scheme = HTTPBearer(auto_error=False)


@inject
def get_current_user(
    # token: str = Depends(oauth2_scheme),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    supabase_db: SupabaseDatabase = Depends(
        Provide[ApplicationContainer.database.supabase_db]
    ),
    user_repo: UserRepository = Depends(
        Provide[ApplicationContainer.repositories.user_repository]
    ),
) -> Optional[UserResponse]:
    '''Dependency returns authenticated user from Supabase token.'''
    try:
        sb = supabase_db.get_client()
        token = credentials.credentials if credentials else None
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not authenticated',
            )

        # 1. Authenticate token with Supabase Auth
        auth_res = sb.auth.get_user(token)
        if not auth_res or not auth_res.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
            )

        auth_user = auth_res.user

        # 2. (Optional) Get additional profile from 'users' table
        try:
            profile = user_repo.find_by_email(auth_user.email)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Error when getting user profile: ' + str(e),
            )

        return profile

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Could not validate credentials: {e}',
        )
