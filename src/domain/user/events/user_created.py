from dataclasses import dataclass
from uuid import UUID

from src.domain.common.events import Event


@dataclass(frozen=True)
class UserCreated(Event):
    user_id: UUID
    username: str
    first_name: str
    last_name: str
    middle_name: str | None
    department: str | None
    role: str
    password: str
