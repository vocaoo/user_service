from dataclasses import dataclass
from enum import Enum

from src.application.common.dto import DTO
from src.domain.common.const import Empty


class SortOrder(Enum):
    ASC = "ASC"
    DESC = "DESC"


@dataclass(frozen=True)
class Pagination:
    offset: int | Empty = Empty.UNSET
    limit: int | Empty = Empty.UNSET
    order: SortOrder = SortOrder.ASC


@dataclass(frozen=True)
class PaginationResult(DTO):
    offset: int | None
    limit: int | None
    total: int
    order: SortOrder

    @classmethod
    def from_pagination(cls, pagination: Pagination, total: int) -> "PaginationResult":
        offset = pagination.offset if pagination.offset is not Empty.UNSET else None
        limit = pagination.limit if pagination.limit is not Empty.UNSET else None
        return cls(offset=offset, limit=limit, order=pagination.order, total=total)


@dataclass(frozen=True)
class PaginatedItemsDTO[Item](DTO):
    data: list[Item]
    pagination: PaginationResult
