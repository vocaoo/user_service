from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar
from uuid import UUID

from uuid6 import uuid7


@dataclass(frozen=True, kw_only=True)
class IntegrationEvent:
    event_id: UUID = field(default_factory=uuid7)
    event_timestamp: datetime = field(default_factory=datetime.utcnow)
    event_type: ClassVar[str]
    exchange_name: ClassVar[str]
    routing_key: ClassVar[str]


def integration_event[EventType: IntegrationEvent](
    event_type: str,
    exchange: str,
    routing_key: str | None = None
) -> Callable[[EventType], EventType]:
    def _integration_event(cls: EventType) -> EventType:
        cls.event_type = event_type
        cls.exchange_name = exchange
        cls.routing_key = routing_key if routing_key is not None else event_type
        return cls
    return _integration_event
