from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustConnection, AbstractConnection, AbstractChannel
from aio_pika.pool import Pool

from .config import EventBusConfig


class ConnectionFactory:
    def __init__(self, config: EventBusConfig) -> None:
        self._config = config

    async def get_connection(self) -> AbstractRobustConnection:
        return await connect_robust(
            host=self._config.host,
            port=self._config.port,
            login=self._config.login,
            password=self._config.password,
        )


class ChannelFactory:
    def __init__(self, rq_connection_pool: Pool[AbstractConnection]) -> None:
        self._rq_connection_pool = rq_connection_pool

    async def get_channel(self) -> AbstractChannel:
        async with self._rq_connection_pool.acquire() as connection:
            return await connection.channel(publisher_confirms=False)
