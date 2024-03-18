from dataclasses import dataclass
from uuid import UUID

from src.infrastructure.event_bus.exchanges import USER_EXCHANGE

from .base import IntegrationEvent, integration_event


@dataclass(frozen=True)
@integration_event("DepartmentDeleted", exchange=USER_EXCHANGE)
class DepartmentDeleted(IntegrationEvent):
    user_id: UUID
