import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.interfaces.persistence import UserRepo
from src.domain.user.value_objects import UserID


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DeletePhotoURL(Command[None]):
    user_id: UUID


class DeletePhotoURLHandler(CommandHandler[DeletePhotoURL, None]):
    def __init__(
        self,
        user_repo: UserRepo,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self._user_repo = user_repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: DeletePhotoURL) -> None:
        user_id = UserID(command.user_id)

        user = await self._user_repo.acquire_user_by_id(user_id)
        user.delete_photo_url()
        await self._user_repo.update_user(user)
        await self._mediator.publish(user.pull_events())
        await self._uow.commit()

        logger.info("User photo deleted", extra={"user": user})
