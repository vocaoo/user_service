import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.interfaces.persistence import UserRepo
from src.domain.user.value_objects import UserID, Password


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SetPassword(Command[None]):
    user_id: UUID
    password: str


class SetPasswordHandler(CommandHandler[SetPassword, None]):
    def __init__(
        self,
        user_repo: UserRepo,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self._user_repo = user_repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: SetPassword) -> None:
        user_id = UserID(command.user_id)
        password = Password(command.password)

        user = await self._user_repo.acquire_user_by_id(user_id)
        user.set_password(password)
        await self._user_repo.update_user(user)
        await self._mediator.publish(user.pull_events())
        await self._uow.commit()

        logger.info("Password updated", extra={"user": user})
