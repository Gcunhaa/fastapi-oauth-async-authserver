from fastapi import APIRouter

from .endpoints import users,token,confirm_email,change_password

router = APIRouter()
router.include_router(router=token.router, tags=['auth'])
router.include_router(router=users.router,prefix="/users", tags = ['user'])
router.include_router(router=confirm_email.router, prefix="/confirmemail", tags=['auth'])
router.include_router(router=change_password.router, prefix='/changepassword', tags=['auth'])