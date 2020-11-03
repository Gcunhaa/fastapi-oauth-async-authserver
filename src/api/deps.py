from os import access
from core.security import get_token_from_header, decode_access_token
from fastapi import Header, HTTPException, Depends

class AuthBaseDependencie:
    
    def __init__(self, authorization : str = Header(None)):
        self.authorization : str = authorization 

def verify_token(auth : AuthBaseDependencie = Depends(AuthBaseDependencie)):
    token = get_token_from_header(auth.authorization)
    if not token:
        raise HTTPException(400, {'error':'invalid_request', 'error_description':'Invalid authentification credentials.'})
    return token

def get_current_user_id(token : str = Depends(verify_token)):
    data = decode_access_token(token)
    return data['sub']