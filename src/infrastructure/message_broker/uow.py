from aio_pika.abc import AbstractTransaction
from aiormq import AMQPError

from src.application.common.exceptions import CommitError, RollbackError
from src.application.common.interfaces import UnitOfWork


class RabbitMQUoW(UnitOfWork):
    def __init__(self, transaction: AbstractTransaction) -> None:
        self._transaction = transaction

    async def commit(self) -> None:
        try:
            await self._transaction.commit()
        except AMQPError as err:
            raise CommitError from err

    async def rollback(self) -> None:
        try:
            await self._transaction.rollback()
        except AMQPError as err:
            raise RollbackError from err
