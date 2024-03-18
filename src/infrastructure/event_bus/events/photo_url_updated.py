from dataclasses import dataclass
from uuid import UUID

from src.infrastructure.event_bus.exchanges import USER_EXCHANGE

from .base import IntegrationEvent, integration_event


@dataclass(frozen=True)
@integration_event("PhotoURLUpdated", exchange=USER_EXCHANGE)
class PhotoURLUpdated(IntegrationEvent):
    user_id: UUID
    photo_url: str
