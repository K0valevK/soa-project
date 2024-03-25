from api.auth.oauth import authenticate_user, create_access_token
from crud.user import get_user
from datetime import datetime, timedelta
from database import get_db_session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas import Token, DataToken
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

router = APIRouter(
    tags=["Authentication"],
)


@router.post('/login')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: AsyncSession = Depends(get_db_session)) -> Token:
    user = await get_user(db, form_data.username)
    user = authenticate_user(user, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
