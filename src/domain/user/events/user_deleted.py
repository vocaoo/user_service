from dataclasses import dataclass
from uuid import UUID

from src.domain.common.events import Event


@dataclass(frozen=True)
class UserDeleted(Event):
    user_id: UUID
