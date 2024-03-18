from dataclasses import dataclass
from uuid import UUID

from src.infrastructure.event_bus.exchanges import USER_EXCHANGE

from .base import IntegrationEvent, integration_event


@dataclass(frozen=True)
@integration_event("RoleUpdated", exchange=USER_EXCHANGE)
class RoleUpdated(IntegrationEvent):
    user_id: UUID
    role: str
