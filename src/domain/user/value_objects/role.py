from dataclasses import dataclass
from enum import Enum

from src.domain.common.exceptions import DomainException
from src.domain.common.value_objects import ValueObject


@dataclass(eq=False)
class WrongRoleValue(DomainException):
    role: str


class NonexistentRole(WrongRoleValue):
    @property
    def message(self) -> str:
        return f'NONEXISTENT ROLE "{self.role}"'


class Roles(Enum):
    EXECUTOR = "Исполнитель"
    OPERATOR = "Оператор"
    DIRECTOR = "Руководитель"
    ADMIN = "Администратор"


@dataclass(frozen=True)
class Role(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if self.value not in Roles:
            raise NonexistentRole(self.value)
