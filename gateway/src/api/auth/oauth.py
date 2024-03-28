from datetime import timedelta, datetime

from asyncio import run
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession


from src.config import settings
from src.crud.user import get_user
from src.database import get_db_session
from src.schemas import Token, DataToken

SECRET_KEY = settings.oauth_token_secret
ALGORITHM = 'HS256'
EXPIRE_TIME = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_TIME)
    to_encode.update({'expire': expire.strftime("%Y-%m-%d %H:%M:%S")})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        login: str = payload.get('login')
        if login is None:
            raise credentials_exception
        token_data = DataToken(login=login)

    except JWTError as e:
        print(e)
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db_session)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail='Could not validate credentials',
                                          headers={'WWW-Authenticate': 'Bearer'})
    token_data = verify_token(token, credentials_exception)
    user = run(get_user(db, token_data.login))

    return user
