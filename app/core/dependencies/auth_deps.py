from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dependency_injector.wiring import inject, Provide

from app.core.containers.application_container import ApplicationContainer
from app.db.databases.supabase import SupabaseDatabase
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


@inject
def get_current_user(
    token: str = Depends(oauth2_scheme),
    supabase_db: SupabaseDatabase = Depends(
        Provide[ApplicationContainer.database.supabase_db]
    ),
    user_repo: UserRepository = Depends(
        Provide[ApplicationContainer.repositories.user_repository]
    ),
):
    '''Dependency returns authenticated user from Supabase token.'''
    try:
        sb = supabase_db.get_client()

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
                detail='Error when getting user profile',
            )

        return {
            'auth_user': auth_user.model_dump(),
            'profile': profile.model_dump() if profile else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Could not validate credentials: {e}',
        )
