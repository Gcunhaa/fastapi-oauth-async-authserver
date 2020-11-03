from fastapi import Form, HTTPException, Depends
from models.user import User, db
from models.refresh_token import RefreshToken
import secrets
from datetime import timedelta, datetime
from core.config import settings
from sqlalchemy import and_
from jwcrypto import jwk, jwt

private_key = None

with open('core/keys/private.pem', 'rb') as pemfile:
    private_key = jwk.JWK.from_pem(pemfile.read(), password='vertrigo'.encode('utf-8'))

class AuthLoginForm:
    
    def __init__(
        self,
        grant_type: str = Form(...),
        username: str = Form(None),
        password: str = Form(None),
        refresh_token : str = Form(None)
    ):
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.refresh_token = refresh_token


async def verify_auth_form(form_data : AuthLoginForm = Depends(AuthLoginForm)) -> AuthLoginForm:
    if form_data.grant_type != 'password' and form_data.grant_type != 'refresh_token':
        raise HTTPException(status_code=400, detail={'error': 'invalid_request'})

    if form_data.grant_type == 'password':
        if form_data.username == None or form_data.password == None or form_data.refresh_token != None:
            raise HTTPException(status_code=400, detail={'error': 'invalid_request'})

    elif form_data.grant_type == 'refresh_token':
        if form_data.refresh_token == None or form_data.username != None or form_data.password != None:
            raise HTTPException(status_code=400, detail={'error': 'invalid_request'})
    
    return form_data


async def create_refresh_token(user : User) -> str:
    token : str = secrets.token_hex(16)

    refresh_token : RefreshToken = RefreshToken(
        user_id= user.id,
        valid_until= datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRATION_TIME),
        token=token
    )

    await refresh_token.create()
    print(token)
    return token

async def verify_refresh_token(refresh_token : str) -> bool:
    founding_token : RefreshToken =  await RefreshToken.query.where(RefreshToken.token == refresh_token).gino.first() 
    
    if founding_token.valid_until <= datetime.utcnow():
        await founding_token.delete()
        return False
    else:
        return True

async def get_owner_refresh_token(refresh_token : str) -> User:
    founding_token : RefreshToken =  await RefreshToken.query.where(RefreshToken.token == refresh_token).gino.first() 
    return await User.get(founding_token.user_id)

def authentificate(email : str, password: str) -> User:
    user : User = User.query.where(User.email == email).gino.first()

    if user != None and user.password == password:
        return user
    else : 
        return None

def create_access_token(user : User) -> str:
    header = {
        "alg": "RS256",
        "typ": "JWT"
    }

    exp = datetime.utcnow() + timedelta(settings.ACCESS_TOKEN_EXPIRATION_TIME)

    payload = {
        "sub" : user.id,
        "iat" : datetime.utcnow().timestamp(),
        "exp" : exp.timestamp(),
        "superuser": user.is_superuser,
    }

    token = jwt.JWT(header=header, claims=payload)
    token.make_signed_token(key=private_key)
    return token.serialize()

def decode_access_token(access_token : str)-> str:
    token = jwt.JWT.deserialize(access_token, key=private_key)
    return token.claims

def get_token_from_header(token : str) -> str:
    print(token)
    data = token.split()
    print(data)
    if data[0] == "Bearer" and len(data) == 2:
        return data[1]
    
    return ''