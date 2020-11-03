from datetime import datetime

from typing import Optional

from pydantic import BaseModel, EmailStr

class AuthorizationResponse(BaseModel):
    access_token : str =''
    token_type : str = ''
    expires_in : int = 0
    refresh_token : str = ''

