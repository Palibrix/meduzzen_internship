import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException, format_number, PhoneNumberFormat
from pydantic import BaseModel, EmailStr, constr, field_validator, AnyUrl, Field
from typing import List, Optional


class UserBase(BaseModel):
    user_email: EmailStr
    user_firstname: constr(min_length=1, max_length=100)
    user_lastname: constr(min_length=1, max_length=100)
    user_city: Optional[constr(min_length=1, max_length=100)]
    user_phone: Optional[str]
    user_avatar: Optional[str]

    @field_validator('user_phone')
    def validate_phone(cls, field):
        if field is not None:
            try:
                field = phonenumbers.parse(field)
                if not phonenumbers.is_valid_number(field):
                    raise ValueError('Invalid phone number')
                field = format_number(field, PhoneNumberFormat.E164)
            except NumberParseException as e:
                raise ValueError(f'An error occurred while parsing the phone number: {str(e)}')
            except Exception as e:
                raise ValueError(f'An unexpected error occurred: {str(e)}')
        return field


class User(UserBase):
    user_id: int = Field(..., gt=0)
    is_active: bool
    is_superuser: bool


class SignInRequest(BaseModel):
    user_email: EmailStr
    hashed_password: str


class SignUpRequest(UserBase):
    hashed_password: str


class UserUpdateRequest(BaseModel):
    user_firstname: Optional[constr(min_length=1, max_length=100)] = None
    user_lastname: Optional[constr(min_length=1, max_length=100)] = None
    hashed_password: Optional[str] = None


class UserUpdateResponse(BaseModel):
    user_firstname: Optional[str] = None
    user_lastname: Optional[str] = None


class UsersListResponse(BaseModel):
    users: List[User]


class UserDetailResponse(User):
    pass


class UserAuth0CreateRequest(BaseModel):
    user_email: EmailStr
