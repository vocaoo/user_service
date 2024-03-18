from dataclasses import dataclass, field
from typing import Self

from src.domain.common.entities import AggregateRoot
from src.domain.user import events
from src.domain.user.exceptions import UsernameAlreadyExists, UserIsDeleted
from src.domain.user.value_objects import (
    DeletionTime,
    Department,
    FullName,
    Password,
    PhotoURL,
    Role,
    UserID,
    Username
)


@dataclass
class User(AggregateRoot):
    user_id: UserID
    username: Username
    full_name: FullName
    department: Department
    role: Role
    password: Password
    photo_url: PhotoURL = field(default=PhotoURL(None))
    existing_usernames: set[Username] = field(default_factory=set)
    deleted_at: DeletionTime = field(default=DeletionTime.create_not_deleted(), kw_only=True)

    @classmethod
    def create_user(
        cls,
        user_id: UserID,
        username: Username,
        full_name: FullName,
        role: Role,
        password: Password,
        existing_usernames: set[Username],
        department: Department = Department(None)
    ) -> Self:
        if username in existing_usernames:
            raise UsernameAlreadyExists(username.to_raw())

        existing_usernames.add(username)
        user = cls(
            user_id=user_id,
            username=username,
            full_name=full_name,
            department=department,
            role=role,
            password=password,
            existing_usernames=existing_usernames
        )
        user.record_event(
            events.UserCreated(
                user_id=user_id.to_raw(),
                username=username.to_raw(),
                first_name=full_name.first_name,
                last_name=full_name.last_name,
                middle_name=full_name.middle_name,
                department=department.to_raw(),
                role=role.to_raw(),
                password=password.to_raw(),
            )
        )

        return user

    def set_username(self, username: Username) -> None:
        self._validate_not_deleted()

        if self.username != username:
            if username in self.existing_usernames:
                raise UsernameAlreadyExists(username.to_raw())

            self.existing_usernames.remove(self.username)
            self.existing_usernames.add(username)
            self.username = username

        self.record_event(
            events.UsernameUpdated(
                user_id=self.user_id.to_raw(),
                username=self.username.to_raw()
            )
        )

    def set_full_name(self, full_name: FullName) -> None:
        self._validate_not_deleted()

        self.full_name = full_name
        self.record_event(
            events.FullNameUpdated(
                user_id=self.user_id.to_raw(),
                first_name=self.full_name.first_name,
                last_name=self.full_name.last_name,
                middle_name=self.full_name.middle_name
            )
        )

    def set_role(self, role: Role) -> None:
        self._validate_not_deleted()

        self.role = role
        self.record_event(
            events.RoleUpdated(
                user_id=self.user_id.to_raw(),
                role=self.role.to_raw()
            )
        )

    def set_department(self, department: Department) -> None:
        self._validate_not_deleted()

        self.department = department
        self.record_event(
            events.DepartmentUpdated(
                user_id=self.user_id.to_raw(),
                department=self.department.to_raw()
            )
        )

    def set_photo_url(self, photo_url: PhotoURL) -> None:
        self._validate_not_deleted()

        self.photo_url = photo_url
        self.record_event(
            events.PhotoURLUpdated(
                user_id=self.user_id.to_raw(),
                photo_url=self.photo_url.to_raw()
            )
        )

    def set_password(self, password: Password) -> None:
        self._validate_not_deleted()

        self.password = password
        self.record_event(
            events.PasswordUpdated(
                user_id=self.user_id.to_raw(),
                password=self.password.to_raw()
            )
        )

    def delete_user(self) -> None:
        self._validate_not_deleted()

        self.existing_usernames.remove(self.username)
        self.username = Username(None)
        self.deleted_at = DeletionTime.create_deleted()
        self.record_event(
            events.UserDeleted(
                user_id=self.user_id.to_raw()
            )
        )

    def delete_department(self) -> None:
        self._validate_not_deleted()

        self.department = Department(None)
        self.record_event(
            events.DepartmentDeleted(
                user_id=self.user_id.to_raw()
            )
        )

    def delete_photo_url(self) -> None:
        self._validate_not_deleted()

        self.photo_url = PhotoURL(None)
        self.record_event(
            events.PhotoURLDeleted(
                user_id=self.user_id.to_raw()
            )
        )

    def _validate_not_deleted(self) -> None:
        if self.deleted_at.is_deleted():
            raise UserIsDeleted(self.user_id.to_raw())
