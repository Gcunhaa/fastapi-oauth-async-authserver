from pydantic import BaseModel


class HealthyError(BaseModel):
    error: str = ""
    description: str = ""
