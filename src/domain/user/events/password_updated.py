from dataclasses import dataclass
from uuid import UUID

from src.domain.common.events import Event


@dataclass(frozen=True)
class PasswordUpdated(Event):
    user_id: UUID
    password: str
