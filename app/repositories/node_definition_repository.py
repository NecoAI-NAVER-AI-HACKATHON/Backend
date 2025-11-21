from contextlib import AbstractContextManager
from typing import Callable

from sqlmodel import Session

from app.models.node_definition import NodeDefinition
from app.repositories.base_repository import BaseRepository


class NodeDefinitionRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, NodeDefinition)
