from datetime import datetime

from typing import Optional

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    fullname: Optional[str] = None

class UserOut(UserBase):
    created: Optional[datetime] = None
    last_updated: Optional[datetime] = None

class UserCreateIn(UserBase):
    fullname: str
    email: EmailStr
    password : str

class UserUpdateIn(UserBase):
    password : Optional[str] = None


#DATABASE BASE
class UserInDBBase(UserBase):
    id: Optional[int] = None
    created: Optional[datetime] = None
    last_updated: Optional[datetime] = None

    class Config:
        orm_mode = True

class UserInDb(UserInDBBase):
    pass

