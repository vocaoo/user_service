from typing import Union

from src.application.common.exceptions import MappingError
from src.domain.user.events import (
    DepartmentDeleted,
    DepartmentUpdated,
    FullNameUpdated,
    PasswordUpdated,
    PhotoURLDeleted,
    PhotoURLUpdated,
    RoleUpdated,
    UsernameUpdated,
    UserCreated,
    UserDeleted
)

from . import events as integration_events


DomainEvent = Union[
    UserCreated, UserDeleted,
    DepartmentUpdated, DepartmentDeleted,
    FullNameUpdated, PasswordUpdated,
    PhotoURLDeleted, PhotoURLUpdated,
    RoleUpdated, UsernameUpdated
]


def convert_user_created_to_integration(
    event: UserCreated
) -> integration_events.UserCreated:
    return integration_events.UserCreated(
        user_id=event.user_id,
        username=event.username,
        first_name=event.first_name,
        last_name=event.last_name,
        middle_name=event.middle_name,
        department=event.department,
        role=event.role,
        password=event.password,
    )


def convert_user_deleted_to_integration(
    event: UserDeleted
) -> integration_events.UserDeleted:
    return integration_events.UserDeleted(
        user_id=event.user_id,
    )


def convert_department_updated_to_integration(
    event: DepartmentUpdated
) -> integration_events.DepartmentUpdated:
    return integration_events.DepartmentUpdated(
        user_id=event.user_id,
        department=event.department,
    )


def convert_department_deleted_to_integration(
    event: DepartmentDeleted
) -> integration_events.DepartmentDeleted:
    return integration_events.DepartmentDeleted(
        user_id=event.user_id,
    )


def convert_full_name_updated_to_integration(
    event: FullNameUpdated
) -> integration_events.FullNameUpdated:
    return integration_events.FullNameUpdated(
        user_id=event.user_id,
        first_name=event.first_name,
        last_name=event.last_name,
        middle_name=event.middle_name,
    )


def convert_password_updated_to_integration(
    event: PasswordUpdated
) -> integration_events.PasswordUpdated:
    return integration_events.PasswordUpdated(
        user_id=event.user_id,
        password=event.password,
    )


def convert_photo_url_deleted_to_integration(
    event: PhotoURLDeleted
) -> integration_events.PhotoURLDeleted:
    return integration_events.PhotoURLDeleted(
        user_id=event.user_id,
    )


def convert_photo_url_updated_to_integration(
    event: PhotoURLUpdated
) -> integration_events.PhotoURLUpdated:
    return integration_events.PhotoURLUpdated(
        user_id=event.user_id,
        photo_url=event.photo_url,
    )


def convert_role_updated_to_integration(
    event: RoleUpdated
) -> integration_events.RoleUpdated:
    return integration_events.RoleUpdated(
        user_id=event.user_id,
        role=event.role,
    )


def convert_username_updated_to_integration(
    event: UsernameUpdated
) -> integration_events.UsernameUpdated:
    return integration_events.UsernameUpdated(
        user_id=event.user_id,
        username=event.username,
    )


def convert_domain_event_to_integration(
    event: DomainEvent
) -> integration_events.IntegrationEvent:
    match event:
        case UserCreated():
            return convert_user_created_to_integration(event)
        case UserDeleted():
            return convert_user_deleted_to_integration(event)
        case DepartmentUpdated():
            return convert_department_updated_to_integration(event)
        case DepartmentDeleted():
            return convert_department_deleted_to_integration(event)
        case FullNameUpdated():
            return convert_full_name_updated_to_integration(event)
        case PasswordUpdated():
            return convert_password_updated_to_integration(event)
        case PhotoURLUpdated():
            return convert_photo_url_updated_to_integration(event)
        case PhotoURLDeleted():
            return convert_photo_url_deleted_to_integration(event)
        case RoleUpdated():
            return convert_role_updated_to_integration(event)
        case UsernameUpdated():
            return convert_username_updated_to_integration(event)
        case _:
            raise MappingError(f"Event {event} can't be mapped to integration event")
