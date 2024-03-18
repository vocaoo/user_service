from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from src.application.common.pagination import Pagination
from src.application.user.dto import UserDTOs, User, Users
from src.domain.common.const import Empty


@dataclass(frozen=True)
class GetUserFilters:
    deleted: bool | Empty = Empty.UNSET


class UserReader(Protocol):
    async def get_user_by_id(self, user_id: UUID) -> UserDTOs:
        raise NotImplementedError

    async def get_user_by_username(self, username: str) -> User:
        raise NotImplementedError

    async def get_users(self, filters: GetUserFilters, pagination: Pagination) -> Users:
        raise NotImplementedError
