from dataclasses import dataclass
from uuid import UUID

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class UserID(ValueObject[UUID]):
    value: UUID
