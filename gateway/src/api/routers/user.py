from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db_session
from src.crud.user import get_user, create_user, fill_info
from src.schemas.user import User, UserCreate, UserUpdate
from src.schemas.token import Token, DataToken
from src.api.auth.oauth import oauth2_scheme
from src.api.auth.oauth import create_token
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import hashlib

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/signup", response_model=User)
async def new_user(user: UserCreate, db: AsyncSession = Depends(get_db_session)):
    db_user = await get_user(db, user.login)
    if db_user:
        raise HTTPException(status_code=400, detail="Login already exists")
    return await create_user(db, user)


@router.post("/{user_login}", response_model=User)
async def upd_user(user_login: str, args: UserUpdate, db: AsyncSession = Depends(get_db_session)):
    db_user = await get_user(db, user_login)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await fill_info(db, user_login, args)


'''
@router.get("/{user_login}", response_model=User)
async def user_details(user_login: str, db: AsyncSession = Depends(get_db_session)):
    result = await get_user(db, user_login)
    return result
'''


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db_session)):
    db_user = await get_user(db, form_data.username)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='The user does not exist')

    if hashlib.md5(form_data.password.encode()).hexdigest() != db_user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid password')

    access_token: str = create_token(data={'login': db_user.login})
    return Token(access_token=access_token, token_type='bearer')
