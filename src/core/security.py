
from fastapi import Form, HTTPException, Depends
from models.user import User, db
from models.refresh_token import RefreshToken
from models.pre_user import PreUser
from models.confirm_email_token import ConfirmEmailToken
from models.change_password_token import ChangePasswordToken
import secrets
from datetime import timedelta, datetime
from core.config import settings
from sqlalchemy import and_
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import re

private_key = None
public_key = None
#TODO: Pegar private e public key do S3 AWS
with open('core/keys/private.pem', 'rb') as pemfile:
    private_key = serialization.load_pem_private_key(data=pemfile.read(),password=b'vertrigo',backend=default_backend())


#TODO: Pegar private e public key do S3 AWS
with open('core/keys/public.pem', 'rb') as pemfile:
    public_key = serialization.load_pem_public_key(data=pemfile.read(),backend=default_backend())

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

    exp = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION_TIME)
    payload = {
        "sub" : user.id,
        "iat" : datetime.utcnow().timestamp(),
        "exp" : exp.timestamp(),
        "superuser": user.is_superuser,
    }

    token = jwt.encode(payload=payload, key=private_key, algorithm='RS256')
    return token.decode('utf-8')

def decode_access_token(access_token : str)-> dict:
    token = jwt.decode(jwt=access_token, key=public_key)
    return token

def get_token_from_header(token : str) -> str:
    data = token.split()

    if data[0] == "Bearer" and len(data) == 2:
        return data[1]
    
    return ''


"""[summary]

    Minimum 8 characters.
    The alphabets must be between [a-z]
    At least one alphabet should be of Upper Case [A-Z]
    At least 1 number or digit between [0-9].

"""
def is_password_valid(password : str) -> bool:
    if (len(password)<8): 
        return False
    elif not re.search("[a-z]", password):
        return False
    elif not re.search("[A-Z]", password): 
        return False
    elif not re.search("[0-9]", password): 
        return False
    elif re.search("\s", password): 
        return False
    else: 
        return True

async def create_email_confirmation_token(user : PreUser) -> str:
    token : str = secrets.token_hex(16)

    confirm_email_token : ConfirmEmailToken = ConfirmEmailToken(
        pre_user_id= user.id,
        valid_until= datetime.utcnow() + timedelta(minutes=settings.EMAIL_CONFIRMATION_TOKEN_EXPIRATION_TIME),
        token=token
    )

    await confirm_email_token.create()
    return token

async def create_password_change_token(user : User) -> str:
    token : str = secrets.token_hex(16)

    change_password_token : ChangePasswordToken = ChangePasswordToken(
        user_id= user.id,
        valid_until= datetime.utcnow() + timedelta(minutes=settings.EMAIL_CONFIRMATION_TOKEN_EXPIRATION_TIME),
        token=token
    )

    await change_password_token.create()
    return token
