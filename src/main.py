from fastapi import FastAPI
from core.config import settings
from gino.ext.starlette import Gino

app : FastAPI = FastAPI(title=settings.PROJECT_NAME,version=settings.VERSION)
db : Gino = Gino(dsn=settings.get_postgres_dsn())

db.init_app(app)


from api.api_v1.api import router

app.include_router(router, prefix=settings.API_VERSION_STR, tags=['Users'])
