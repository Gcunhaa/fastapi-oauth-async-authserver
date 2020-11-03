from fastapi import APIRouter

from .endpoints import users,token

router = APIRouter()
router.include_router(router=token.router)
router.include_router(router=users.router,prefix="/users")
