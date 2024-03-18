from dataclasses import dataclass
from uuid import UUID

from src.domain.common.exceptions import DomainException


@dataclass(eq=False)
class UserIsDeleted(RuntimeError, DomainException):
    user_id: UUID

    @property
    def title(self) -> str:
        return f'The user with "{self.user_id}" user_id is deleted'


@dataclass(eq=False)
class UsernameAlreadyExists(DomainException):
    username: str | None = None

    @property
    def title(self) -> str:
        if self.username is not None:
            return f'A user with the "{self.username}" username already exists'
        return "A user with the username already exists"
