from pydantic import BaseModel
from typing import List, Optional


class UserBase(BaseModel):
    user_email: str
    user_firstname: str
    user_lastname: str
    user_city: Optional[str]
    user_phone: Optional[str]
    user_avatar: Optional[str]


class User(UserBase):
    user_id: int
    is_active: bool
    is_superuser: bool


class SignInRequest(BaseModel):
    user_email: str
    hashed_password: str


class SignUpRequest(UserBase):
    hashed_password: str


class UserUpdateRequest(BaseModel):
    user_firstname: Optional[str] = None
    user_lastname: Optional[str] = None
    user_city: Optional[str] = None
    user_phone: Optional[str] = None
    user_avatar: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UsersListResponse(BaseModel):
    users: List[User]


class UserDetailResponse(User):
    pass
