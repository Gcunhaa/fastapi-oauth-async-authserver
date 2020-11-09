from pydantic import BaseSettings, EmailStr
from sqlalchemy.engine.url import URL


class Settings(BaseSettings):
    API_VERSION_STR: str = "/v1"
    PROJECT_NAME: str = "AuthServer"
    VERSION: str = "0.0.0"

    POSTGRES_SERVER: str = "lallah.db.elephantsql.com"
    POSTGRES_USER: str = "qifealev"
    POSTGRES_PASSWORD: str = "tnmtOSFsY0yf46nLNcoF_Q3QKVRTkVuF"
    POSTGRES_DB: str = "qifealev"
    POSTGRES_PORT: int = 5432

    REFRESH_TOKEN_EXPIRATION_TIME: int = 7  # IN DAYS
    ACCESS_TOKEN_EXPIRATION_TIME: int = 5  # IN MINUTES
    EMAIL_CONFIRMATION_TOKEN_EXPIRATION_TIME: int = 30  # In minutes
    PASSWORD_CHANGE_TOKEN_EXPIRATION_TIME: int = 30  # In minutes

    SMTP_HOSTNAME: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_NO_REPLY_EMAIL: EmailStr

    class Config:
        case_sensitive = True

    def get_postgres_dsn(self):
        return f"asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    def get_alembic_dsn(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"


settings = Settings()
