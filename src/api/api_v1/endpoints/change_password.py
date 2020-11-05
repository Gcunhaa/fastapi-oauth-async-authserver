from datetime import datetime
from core.security import is_password_valid
from typing import Any, List, Optional, Union

from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy import and_
from schemas.error import HealthyError
from schemas.success import Success
from schemas.authorization import AuthorizationResponse
from models.change_password_token import ChangePasswordToken
from models.user import User
from core.security import create_password_change_token
from core.config import settings
from pydantic import EmailStr

router = APIRouter()

@router.post('/password/{token}')
async def change_password(token : str, new_password: str):
    token_orm : ChangePasswordToken = await ChangePasswordToken.query.where(ChangePasswordToken.token == token).gino.first()

    if token_orm is None or token_orm.valid_until < datetime.utcnow():
        raise HTTPException(status_code=400, detail={'error':'invalid_grant','error_description':'Invalid token'})
    
    user : User = await User.get_or_404(token_orm.user_id)

    if not is_password_valid(new_password):
        raise HTTPException(status_code=404, detail={'error':'invalid_password', 'error_description':'Invalid password'})

    await token_orm.delete()
    await user.update(password=new_password).apply()
    return {'success' : 'changepassword', 'success_description':'Password changed with success.'}

@router.post('/resetpassword')
async def request_change_password(email : EmailStr):
    user : User = await User.query.where(User.email == email).gino.first()
    
    if user:
        #TODO:SEND EMAIL
        token : str = await create_password_change_token(user)
        print(token)

    return {'success' : 'resetpassword_email', 'success_description':'Email sent with success.'}