from fastapi import APIRouter, HTTPException
from models.refresh_token import RefreshToken

router = APIRouter()


@router.post("/")
async def logout(refresh_token: str):
    token_orm: RefreshToken = await RefreshToken.query.where(
        RefreshToken.token == refresh_token
    ).gino.first()

    if not token_orm:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_grant",
                "error_description": "Invalid refresh token",
            },
        )

    await token_orm.delete()
    return {
        "success": "logout",
        "success_description": "Refresh token revoked with success",
    }
