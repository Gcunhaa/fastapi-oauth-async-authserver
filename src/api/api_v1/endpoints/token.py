from typing import Any, List, Optional, Union

from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy import and_
from schemas.error import HealthyError
from schemas.success import Success
from schemas.authorization import AuthorizationResponse
from models.user import User as ORMUser
from models.pre_user import PreUser
from models.login import LoginLog

from core.security import (
    AuthLoginForm,
    verify_auth_form,
    create_refresh_token,
    verify_refresh_token,
    get_owner_refresh_token,
    create_access_token,
    create_email_confirmation_token,
)
from core.config import settings
from core.email import send_confirmation_email

router = APIRouter()


@router.post("/token", response_model=AuthorizationResponse)
async def get_token(
    request: Request, form_data: AuthLoginForm = Depends(verify_auth_form)
):
    login_log = LoginLog(
        grant_type=form_data.grant_type, ip_address=request.client.host
    )
    response = AuthorizationResponse(
        token_type="Bearer", expires_in=settings.ACCESS_TOKEN_EXPIRATION_TIME
    )
    user: ORMUser = None

    if form_data.grant_type == "password":
        user = await ORMUser.query.where(
            ORMUser.email == form_data.username
        ).gino.first()

        if user is None or form_data.password != user.password:
            if not user:
                pre_user: PreUser = await PreUser.query.where(
                    PreUser.email == form_data.username
                ).gino.first()

                if pre_user and pre_user.password == form_data.password:
                    token: str = await create_email_confirmation_token(pre_user)
                    await send_confirmation_email(pre_user.email, token)
                    return {
                        "pre_user_id": pre_user.id,
                        "success": "emailconfirm_login",
                        "success_description": "Need to confirm email before login",
                    }

            if user.password == None:
                #TODO: AUTENTIFICAR COM GOOGLE,FACEBOOK ou APPLE
                return ''

            raise HTTPException(
                status_code=400,
                detail={
                    "error": "invalid_grant",
                    "error_description": "Email or password incorrect.",
                },
            )

        refresh_token = await create_refresh_token(user)

        response.refresh_token = refresh_token

    if form_data.grant_type == "refresh_token":
        if not await verify_refresh_token(form_data.refresh_token):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "invalid_grant",
                    "error_description": "Refresh token invalid or revoked.",
                },
            )

        user = await get_owner_refresh_token(form_data.refresh_token)
        response.refresh_token = form_data.refresh_token

    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_grant",
                "error_description": "User is not active.",
            },
        )

    login_log.user_id = user.id
    await login_log.create()

    response.access_token = create_access_token(user)
    return response
