from typing import Any, List, Optional, Union

from fastapi import APIRouter, HTTPException, Depends

from core.security import create_email_confirmation_token
from schemas.user import UserCreateIn, UserUpdateIn, UserInDb, UserInDBBase
from schemas.error import HealthyError
from schemas.success import Success
from models.user import User as ORMUser
from core.email import send_confirmation_email
from models.pre_user import PreUser
from api.deps import UserData

router = APIRouter()

@router.get('/', response_model=List[UserInDBBase])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    user_data : UserData = Depends(UserData) 
) -> Any:
    """
        Retrieve users.
    """

    if not user_data.is_superuser:
        raise HTTPException(status_code=403)

    users = await ORMUser.query.limit(limit).offset(skip).gino.all()
    return users

@router.post('/')
async def create_user(
    request : UserCreateIn
) -> Any:
    """
    Create user
    """
    user: ORMUser = await ORMUser.query.where(ORMUser.email == request.email).gino.first()
    
    #Verify if email already in use, and if so throws exception, otherwise create it.
    if user:
        error = HealthyError()
        error.error =  'AlreadyExists'
        error.description = 'Email already in use.'
        return error
    else:
        request.is_active = True
        request.is_superuser = False



        pre_user = await PreUser.create(**request.dict())
        success = Success()
        success.success = "AccountCreated"
        success.description = "Account created with success."
        
        token : str = await create_email_confirmation_token(pre_user)

        await send_confirmation_email(pre_user.email,token)
        
        return success

@router.get('/{id}', response_model=UserInDb)
async def read_user(
    id: int,
    user_data : UserData = Depends()
) -> Any:
    """
    Retrieve user by id
    """
    if user_data.id != id and not user_data.is_superuser:
        raise HTTPException(status_code=403)

    user : ORMUser = await ORMUser.get_or_404(id)
    return UserInDb.from_orm(user)

@router.put('/{id}', response_model=UserInDb)
async def update_user(
    id: int,
    request: UserUpdateIn,
    user_data : UserData = Depends()
) -> Any:
    """
    Update user
    """

    if user_data.id != id and not user_data.is_superuser:
        raise HTTPException(status_code=403)

    user : ORMUser= await ORMUser.get_or_404(id)
    await user.update(**request.dict(skip_defaults=True, exclude_unset=True)).apply()
    return UserInDb.from_orm(user)