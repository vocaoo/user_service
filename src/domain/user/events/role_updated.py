from dataclasses import dataclass
from uuid import UUID

from src.domain.common.events import Event


@dataclass(frozen=True)
class RoleUpdated(Event):
    user_id: UUID
    role: str
