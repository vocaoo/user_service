import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.interfaces.persistence import UserRepo
from src.domain.user.value_objects import UserID, PhotoURL


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SetPhotoURL(Command[None]):
    user_id: UUID
    photo_url: str


class SetPhotoURLHandler(CommandHandler[SetPhotoURL, None]):
    def __init__(
        self,
        user_repo: UserRepo,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self._user_repo = user_repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: SetPhotoURL) -> None:
        user_id = UserID(command.user_id)
        photo_url = PhotoURL(command.photo_url)

        user = await self._user_repo.acquire_user_by_id(user_id)
        user.set_photo_url(photo_url)
        await self._user_repo.update_user(user)
        await self._mediator.publish(user.pull_events())
        await self._uow.commit()

        logger.info("Photo URL updated", extra={"user": user})
