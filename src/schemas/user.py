from datetime import datetime
import re
from typing import Optional
from core.security import is_password_valid
from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = None
    fullname: Optional[str] = None


class UserCreateIn(UserBase):
    fullname: str
    email: EmailStr
    password: str

    @validator("password")
    def validate_password(cls, value):
        if not is_password_valid(value):
            raise ValueError("Password is not valid.")
        return value


class UserUpdateIn(BaseModel):
    is_active: Optional[bool] = True
    fullname: Optional[str] = None


# DATABASE BASE
class UserInDBBase(UserBase):
    id: Optional[int] = None
    created: Optional[datetime] = None
    last_updated: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserInDb(UserInDBBase):
    pass
