from .base import IntegrationEvent, integration_event
from .department_deleted import DepartmentDeleted
from .department_updated import DepartmentUpdated
from .full_name_updated import FullNameUpdated
from .password_updated import PasswordUpdated
from .photo_url_deleted import PhotoURLDeleted
from .photo_url_updated import PhotoURLUpdated
from .role_updated import RoleUpdated
from .user_created import UserCreated
from .user_deleted import UserDeleted
from .username_updated import UsernameUpdated


__all__ = (
    "IntegrationEvent",
    "integration_event",
    "DepartmentDeleted",
    "DepartmentUpdated",
    "FullNameUpdated",
    "PasswordUpdated",
    "PhotoURLDeleted",
    "PhotoURLUpdated",
    "RoleUpdated",
    "UserCreated",
    "UserDeleted",
    "UsernameUpdated",
)
