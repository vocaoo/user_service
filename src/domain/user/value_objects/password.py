import re

from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject
from src.domain.common.exceptions import DomainException


MAX_PASSWORD_LENGTH = 32
MIN_PASSWORD_LENGTH = 8
UPPERCASE_PATTERN = re.compile(r"[A-Z]")
LOWERCASE_PATTERN = re.compile(r"[a-z]")
DIGIT_PATTERN = re.compile(r"\d")
SYMBOL_PATTERN = re.compile(r"\S")


@dataclass(eq=True)
class WrongPasswordValue(DomainException):
    password: str


class TooShortPassword(WrongPasswordValue):
    pass


class TooLongPassword(WrongPasswordValue):
    pass


class NoUpperCaseError(WrongPasswordValue):
    pass


class NoLowerCaseError(WrongPasswordValue):
    pass


class NoDigitError(WrongPasswordValue):
    pass


class NoSymbolError(WrongPasswordValue):
    pass


@dataclass(frozen=True)
class Password(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if MAX_PASSWORD_LENGTH < len(self.value):
            raise TooLongPassword(self.value)
        if MIN_PASSWORD_LENGTH > len(self.value):
            raise TooShortPassword(self.value)
        if UPPERCASE_PATTERN.match(self.value) is None:
            raise NoUpperCaseError(self.value)
        if SYMBOL_PATTERN.match(self.value) is None:
            raise NoSymbolError(self.value)
