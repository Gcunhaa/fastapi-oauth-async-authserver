from datetime import datetime
from core.security import is_password_valid
from typing import Any, List, Optional, Union

from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy import and_
from schemas.error import HealthyError
from schemas.success import Success
from schemas.authorization import AuthorizationResponse
from models.confirm_email_token import ConfirmEmailToken
from models.pre_user import PreUser
from models.user import User
from core.security import AuthLoginForm, verify_auth_form, create_refresh_token, verify_refresh_token, get_owner_refresh_token, create_access_token
from core.config import settings

router = APIRouter()

"""[Confirmar email]

    Responsible for confirme emails 
    @params token

    Raises:
        HTTPException: [Invalid Token]

    Returns:
        [sucess]: [email_confirmed]
"""
@router.post('/{token}')
async def confirm_email(token : str):
    token_orm : ConfirmEmailToken = await ConfirmEmailToken.query.where(ConfirmEmailToken.token == token).gino.first()
    print(token_orm)
    print(token_orm.valid_until)
    print(datetime.utcnow())
    if token_orm is None or token_orm.valid_until < datetime.utcnow():
        raise HTTPException(status_code=400, detail={'error':'invalid_grant','error_description':'Invalid token'})
    
    pre_user : PreUser = await PreUser.get_or_404(token_orm.pre_user_id)

    await token_orm.delete()
    await User.create(
            fullname = pre_user.fullname,
            email = pre_user.email,
            password = pre_user.password,
            is_active = pre_user.is_active,
            is_superuser = pre_user.is_superuser,
            )
            
    await pre_user.delete()

    return {'success':'email_confirmed', 'success_description':'Email confirmed with success'}
