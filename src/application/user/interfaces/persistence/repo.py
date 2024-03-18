from abc import abstractmethod
from typing import Protocol

from src.domain.user.entities import User
from src.domain.user.value_objects import UserID, Username


class UserRepo(Protocol):
    @abstractmethod
    async def acquire_user_by_id(self, user_id: UserID) -> User:
        raise NotImplementedError

    @abstractmethod
    async def add_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_existing_usernames(self) -> set[Username]:
        raise NotImplementedError
