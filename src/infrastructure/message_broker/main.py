from typing import AsyncGenerator

from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractTransaction
from aio_pika.pool import Pool

from .factories import ConnectionFactory, ChannelFactory
from .config import EventBusConfig


async def build_rq_connection_pool(
    event_bus_config: EventBusConfig
) -> AsyncGenerator[Pool[AbstractConnection], None]:
    connection_pool = Pool(ConnectionFactory(event_bus_config).get_connection, max_size=10)
    async with connection_pool:
        yield connection_pool


async def build_rq_channel_pool(
    connection_pool: Pool[AbstractConnection]
) -> AsyncGenerator[Pool[AbstractChannel], None]:
    channel_pool = Pool(ChannelFactory(connection_pool).get_channel, max_size=100)
    async with channel_pool:
        yield channel_pool


async def build_rq_channel(
    channel_pool: Pool[AbstractChannel],
) -> AsyncGenerator[AbstractChannel, None]:
    async with channel_pool.acquire() as chanel:
        yield chanel
        chanel.transaction()


async def build_rq_transaction(
        channel: AbstractChannel,
) -> AbstractTransaction:
    transaction = channel.transaction()
    await transaction.select()
    return transaction
