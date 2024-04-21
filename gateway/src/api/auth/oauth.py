from config import settings
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from schemas import User

import hashlib

SECRET_KEY = settings.oauth_token_secret
ALGORITHM = 'HS256'
EXPIRE_TIME = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def verify_password(plain_password: str, hashed_password: str):
    return hashlib.md5(plain_password.encode()).hexdigest() == hashed_password


def get_password_hash(password: str):
    return hashlib.md5(password.encode()).hexdigest()


def authenticate_user(user: User, password: str):
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
