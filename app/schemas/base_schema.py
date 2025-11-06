from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ModelBaseInfo(BaseModel):
    """Common fields shared by response schemas.

    Includes a UUID `id` and optional `created_at` / `updated_at` timestamps.
    `from_attributes = True` allows creating the schema from ORM / SQLModel
    instances using attribute access.
    """

    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
