from os import access
from core.security import get_token_from_header, decode_access_token, public_key
from fastapi import Header, HTTPException, Depends
import jwt
from jwt.exceptions import ExpiredSignature

class AuthBaseDependencie:
    
    def __init__(self, authorization : str = Header(...)):
        self.authorization : str = authorization 

def verify_token(auth : AuthBaseDependencie = Depends(AuthBaseDependencie)) -> dict:
    token = get_token_from_header(auth.authorization)
    if not token:
        raise HTTPException(400, {'error':'invalid_request', 'error_description':'Invalid authentification credentials.'})
    
    try:
        data = jwt.decode(jwt=token,key=public_key)
    except ExpiredSignature:
        raise HTTPException(400, {'error':'invalid_request', 'error_description':'Expired access token.'})

    return data

class UserData:
    
    def __init__(self, data : dict = Depends(verify_token)):
      self.id = data['sub']
      self.is_superuser = data['superuser']    
