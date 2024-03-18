from pydantic import BaseModel


class SetUsernameData(BaseModel):
    username: str


class SetFullNameData(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None


class SetDepartmentData(BaseModel):
    department: str


class SetPhotoURLData(BaseModel):
    photo_url: str


class SetRoleData(BaseModel):
    role: str


class SetPasswordData(BaseModel):
    password: str
