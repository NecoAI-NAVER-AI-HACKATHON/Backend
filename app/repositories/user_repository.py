from contextlib import AbstractContextManager
from typing import Callable, Optional

from sqlmodel import Session, select

from app.models.user import User
from app.repositories.base_repository import BaseRepository
from app.schemas.user_schema import UserResponse


class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, User)

    def find_by_email(self, email) -> Optional[UserResponse]:
        with self.session_factory() as session:
            statement = select(User).where(User.email == email)
            res = session.scalars(statement).first()
            return UserResponse.model_validate(res) if res else None
