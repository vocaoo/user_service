from dataclasses import dataclass


@dataclass(frozen=True)
class EventBusConfig:
    host: str = "localhost"
    port: int = 15672
    login: str = "admin"
    password: str = "admin"
