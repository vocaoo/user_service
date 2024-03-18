import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces import UnitOfWork
from src.application.user.interfaces.persistence import UserRepo
from src.domain.user.entities import User
from src.domain.user.value_objects import (
    FullName,
    UserID,
    Username,
    Password,
    Department,
    Role,
)


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateUser(Command[UUID]):
    user_id: UUID
    username: str
    first_name: str
    last_name: str
    middle_name: str | None
    department: str | None
    role: str
    password: str


class CreateUserHandler(CommandHandler[CreateUser, UUID]):
    def __init__(
        self,
        user_repo: UserRepo,
        uow: UnitOfWork,    
        mediator: EventMediator,
    ) -> None:
        self._user_repo = user_repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: CreateUser) -> UUID:
        user_id = UserID(command.user_id)
        username = Username(command.username)
        full_name = FullName(command.first_name, command.last_name, command.middle_name)
        department = Department(command.department)
        role = Role(command.role)
        password = Password(command.password)

        existing_usernames = await self._user_repo.get_existing_usernames()
        user = User.create_user(
            user_id, username, full_name, role, password, existing_usernames, department,
        )
        await self._user_repo.add_user(user)
        await self._mediator.publish(user.pull_events())
        await self._uow.commit()

        logger.info("User created", extra={"user": user})

        return command.user_id
