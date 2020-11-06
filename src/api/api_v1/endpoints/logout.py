from typing import Any, List, Optional, Union

from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy import and_
from schemas.error import HealthyError
from schemas.success import Success
from schemas.authorization import AuthorizationResponse
from models.user import User as ORMUser
from models.pre_user import PreUser
from models.login import LoginLog
from models.refresh_token import RefreshToken
from core.security import AuthLoginForm, verify_auth_form, create_refresh_token, verify_refresh_token, get_owner_refresh_token, create_access_token, create_email_confirmation_token
from core.config import settings
from core.email import send_confirmation_email

router = APIRouter()

@router.post('/')
async def get_token(refresh_token : str):
    token_orm : RefreshToken = await RefreshToken.query.where(RefreshToken.token == refresh_token).gino.first()

    if not token_orm:
        raise HTTPException(status_code=400, detail={'error':'invalid_grant','error_description':'Invalid refresh token'})
    
    await token_orm.delete()
    return {'success':'logout', 'success_description':'Refresh token revoked with success'}