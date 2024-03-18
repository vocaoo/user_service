import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces import UnitOfWork
from src.application.user.interfaces.persistence import UserRepo
from src.domain.user.value_objects import UserID, Role


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SetRole(Command[None]):
    user_id: UUID
    role: str


class SetRoleHandler(CommandHandler[SetRole, None]):
    def __init__(
        self,
        user_repo: UserRepo,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self._user_repo = user_repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: SetRole) -> None:
        user_id = UserID(command.user_id)
        role = Role(command.role)

        user = await self._user_repo.acquire_user_by_id(user_id)
        user.set_role(role)
        await self._user_repo.update_user(user)
        await self._mediator.publish(user.pull_events())
        await self._uow.commit()

        logger.info("Role updated", extra={"user": user})
