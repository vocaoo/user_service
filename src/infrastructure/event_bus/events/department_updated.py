from dataclasses import dataclass
from uuid import UUID

from src.infrastructure.event_bus.exchanges import USER_EXCHANGE

from .base import IntegrationEvent, integration_event


@dataclass(frozen=True)
@integration_event("DepartmentUpdated", exchange=USER_EXCHANGE)
class DepartmentUpdated(IntegrationEvent):
    user_id: UUID
    department: str
