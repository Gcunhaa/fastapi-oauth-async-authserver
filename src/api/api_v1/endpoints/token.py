from typing import Any, List, Optional, Union

from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy import and_
from schemas.error import HealthyError
from schemas.success import Success
from schemas.authorization import AuthorizationResponse
from models.user import User as ORMUser
from models.login import LoginLog

from core.security import AuthLoginForm, verify_auth_form, create_refresh_token, verify_refresh_token, get_owner_refresh_token, create_access_token
from core.config import settings

router = APIRouter()

@router.post('/token', response_model= AuthorizationResponse)
async def get_token(request: Request, form_data : AuthLoginForm = Depends(verify_auth_form)):
    login_log = LoginLog(grant_type = form_data.grant_type, ip_address =request.client.host)
    response = AuthorizationResponse(token_type="Bearer", expires_in=settings.ACCESS_TOKEN_EXPIRATION_TIME)
    user : ORMUser = None

    if form_data.grant_type == 'password':
        user =  await ORMUser.query.where(ORMUser.email == form_data.username).gino.first()

        if user is None or form_data.password != user.password:
            raise HTTPException(status_code=400, detail={'error':'invalid_grant','error_description':'Email or password incorrect.'})

        refresh_token = await create_refresh_token(user)

        response.refresh_token = refresh_token

    if form_data.grant_type == 'refresh_token':
        if not await verify_refresh_token(form_data.refresh_token):
            raise HTTPException(status_code=400, detail={'error':'invalid_grant','error_description':'Refresh token invalid or revoked.'})

        user = await get_owner_refresh_token(form_data.refresh_token)
        response.refresh_token = form_data.refresh_token

    login_log.user_id = user.id
    await login_log.create()

    response.access_token = create_access_token(user)
    return response

