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
    hashed_password: Optional[str] = None


class UserUpdateResponse(BaseModel):
    user_firstname: Optional[str] = None
    user_lastname: Optional[str] = None


class UsersListResponse(BaseModel):
    users: List[User]


class UserDetailResponse(User):
    pass


class UserAuth0CreateRequest(BaseModel):
    user_email: str
