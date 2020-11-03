from typing import Any, List, Optional, Union

from fastapi import APIRouter, HTTPException, Depends

from schemas.user import UserOut, UserCreateIn, UserUpdateIn, UserInDb
from schemas.error import HealthyError
from schemas.success import Success
from models.user import User as ORMUser
from api.deps import get_current_user_id

router = APIRouter()

@router.get('/', response_model=List[UserOut])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user_id  = Depends(get_current_user_id) 
) -> Any:
    """
        Retrieve users.
    """

    #todo: Verify if user has authorization
    print(f'user_id : {current_user_id}')
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
        await ORMUser.create(**request.dict())
        success = Success()
        success.success = "AccountCreated"
        success.description = "Account created with success."
        return success

@router.get('/{id}', response_model=UserOut)
async def read_user(
    id: int
) -> Any:
    """
    Retrieve user by id
    """
    #TODO: Verify if user have authorization
    
    user : ORMUser = await ORMUser.get_or_404(id)
    return UserInDb.from_orm(user)

@router.put('/{id}', response_model=UserOut)
async def update_user(
    id: int,
    request: UserUpdateIn
) -> Any:
    """
    Update user
    """

    #TODO: Verify if user have authorization

    user : ORMUser= await ORMUser.get_or_404(id)
    updated_fields : UserInDb = UserInDb.from_orm(request)
    await user.update(**updated_fields.dict(skip_defaults=True)).apply()
    return UserInDb.from_orm(user)