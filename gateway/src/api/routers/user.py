from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db_session
from src.crud.user import get_user, create_user, fill_info
from src.schemas.user import User, UserCreate, UserUpdate
from src.api.auth.auth_handler import signJWT
from fastapi import APIRouter, Depends, HTTPException
import hashlib

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/sign_up", response_model=User)
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


# TODO: Ещё поломан
@router.post("/login")
async def login(user: UserCreate, db: AsyncSession = Depends(get_db_session)):
    db_user = await get_user(db, user.login)
    if db_user.login == user.login and db_user.password == hashlib.md5(user.password.encode()).hexdigest():
        return signJWT(user.login)
