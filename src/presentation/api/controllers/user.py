from typing import Annotated, Union
from uuid import UUID

from didiator import CommandMediator, Mediator, QueryMediator
from fastapi import APIRouter, Depends, Query, status

from src.application.common.pagination.dto import Pagination, SortOrder
from src.application.user import dto
from src.application.user.commands import (
    CreateUser,
    DeleteUser,
    SetFullName,
    SetUsername,
    SetDepartment,
    SetPhotoURL,
    SetRole,
    SetPassword,
    DeleteDepartment,
    DeletePhotoURL,
)
from src.application.user.exceptions import UserIdAlreadyExists, UserIdNotExist, UsernameNotExist
from src.application.user.interfaces.persistence import GetUserFilters
from src.application.user.queries import GetUserById, GetUserByUsername, GetUsers
from src.domain.common.const import Empty
from src.domain.user.exceptions import UserIsDeleted, UsernameAlreadyExists
from src.domain.user.value_objects.full_name import EmptyName, TooLongName, WrongNameFormat
from src.domain.user.value_objects.username import EmptyUsername, TooLongUsername, WrongUsernameFormat
from src.presentation.api.controllers import requests
from src.presentation.api.controllers.responses import ErrorResponse
from src.presentation.api.controllers.responses.base import OkResponse
from src.presentation.api.providers.stub import Stub

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@user_router.post(
    "/",
    responses={
        status.HTTP_201_CREATED: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[Union[TooLongUsername, EmptyUsername, WrongUsernameFormat]],
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse[Union[UsernameAlreadyExists, UserIdAlreadyExists]],
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    create_user_command: CreateUser,
    mediator: Annotated[Mediator, Depends(Stub(Mediator))],
) -> OkResponse[dto.UserDTOs]:
    user_id = await mediator.send(create_user_command)
    user = await mediator.query(GetUserById(user_id=user_id))
    return OkResponse(result=user)


@user_router.get(
    "/@{username}",
    responses={
        status.HTTP_200_OK: {"model": dto.User},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse[UsernameNotExist]},
    },
)
async def get_user_by_username(
    username: str,
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
) -> OkResponse[dto.User]:
    user = await mediator.query(GetUserByUsername(username=username))
    return OkResponse(result=user)


@user_router.get(
    "/{user_id}",
    responses={
        status.HTTP_200_OK: {"model": dto.UserDTOs},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse[UserIdNotExist]},
    },
)
async def get_user_by_id(
    user_id: UUID,
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
) -> OkResponse[dto.UserDTOs]:
    user = await mediator.query(GetUserById(user_id=user_id))
    return OkResponse(result=user)


@user_router.get(
    "/",
)
async def get_users(
    mediator: Annotated[QueryMediator, Depends(Stub(QueryMediator))],
    deleted: bool | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=1000)] = 1000,
    order: SortOrder = SortOrder.ASC,
) -> OkResponse[dto.Users]:
    users = await mediator.query(
        GetUsers(
            filters=GetUserFilters(deleted if deleted is not None else Empty.UNSET),
            pagination=Pagination(
                offset=offset,
                limit=limit,
                order=order,
            ),
        )
    )
    return OkResponse(result=users)


@user_router.put(
    "/{user_id}/username",
    responses={
        status.HTTP_200_OK: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[Union[UserIdNotExist, TooLongUsername, EmptyUsername, WrongUsernameFormat]],
        },
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[Union[UserIsDeleted, UsernameAlreadyExists]]},
    },
)
async def set_user_username(
    user_id: UUID,
    set_user_username_data: requests.SetUsernameData,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    set_user_username_command = SetUsername(user_id=user_id, username=set_user_username_data.username)
    await mediator.send(set_user_username_command)
    return OkResponse()


@user_router.put(
    "/{user_id}/full-name",
    responses={
        status.HTTP_200_OK: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[Union[UserIdNotExist, EmptyName, WrongNameFormat, TooLongName]],
        },
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[UserIsDeleted]},
    },
)
async def set_user_full_name(
    user_id: UUID,
    set_user_full_name_data: requests.SetFullNameData,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    set_user_full_name_command = SetFullName(
        user_id=user_id,
        first_name=set_user_full_name_data.first_name,
        last_name=set_user_full_name_data.last_name,
        middle_name=set_user_full_name_data.middle_name,
    )
    await mediator.send(set_user_full_name_command)
    return OkResponse()


@user_router.put(
    path="/{user_id}/department",
    responses={
        status.HTTP_200_OK: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse[Union[UserIdNotExist]]},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[UserIsDeleted]},
    })
async def set_department(
    user_id: UUID,
    data: requests.SetDepartmentData,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    command = SetDepartment(user_id=user_id, department=data.department)
    await mediator.send(command)
    return OkResponse()


@user_router.put(
    path="/{user_id}/photo",
    responses={
        status.HTTP_200_OK: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse[Union[UserIdNotExist]]},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[UserIsDeleted]},
    })
async def set_photo_url(
    user_id: UUID,
    data: requests.SetPhotoURLData,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    command = SetPhotoURL(user_id=user_id, photo_url=data.photo_url)
    await mediator.send(command)
    return OkResponse()


@user_router.put(
    path="/{user_id}/role",
    responses={
        status.HTTP_200_OK: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse[Union[UserIdNotExist]]},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[UserIsDeleted]},
    }
)
async def set_role(
    user_id: UUID,
    data: requests.SetRoleData,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    command = SetRole(user_id=user_id, role=data.role)
    await mediator.send(command)
    return OkResponse()


@user_router.put(
    path="/{user_id}/password",
    responses={
        status.HTTP_200_OK: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse[Union[UserIdNotExist]]},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[UserIsDeleted]},
    }
)
async def set_password(
    user_id: UUID,
    data: requests.SetPasswordData,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    command = SetPassword(user_id=user_id, password=data.password)
    await mediator.send(command)
    return OkResponse()


@user_router.delete(
    "/{user_id}",
    responses={
        status.HTTP_200_OK: {"model": dto.DeletedUser},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse[UserIdNotExist]},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[UserIsDeleted]},
    },
)
async def delete_user(
    user_id: UUID,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    await mediator.send(DeleteUser(user_id=user_id))
    return OkResponse()


@user_router.delete(
    path="/{user_id}/department",
    responses={
        status.HTTP_200_OK: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse[Union[UserIdNotExist]]},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[UserIsDeleted]},
    }
)
async def delete_department(
    user_id: UUID,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    await mediator.send(DeleteDepartment(user_id=user_id))
    return OkResponse()


@user_router.delete(
    path="/{user_id}/photo",
    responses={
        status.HTTP_200_OK: {"model": dto.User},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse[Union[UserIdNotExist]]},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[UserIsDeleted]},
    }
)
async def delete_photo_url(
    user_id: UUID,
    mediator: Annotated[CommandMediator, Depends(Stub(CommandMediator))],
) -> OkResponse[None]:
    await mediator.send(DeletePhotoURL(user_id=user_id))
    return OkResponse()
