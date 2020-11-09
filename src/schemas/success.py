from pydantic import BaseModel


class Success(BaseModel):
    success: str = ""
    description: str = ""
