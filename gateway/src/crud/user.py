from api.auth.oauth import get_password_hash
from models import User as UserDBModel
from schemas import UserCreate as UserCreateDBSchema
from schemas import UserUpdate as UserUpdateDBSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(db: AsyncSession, user: UserCreateDBSchema):
    hashed_password = get_password_hash(user.password)
    db_user = UserDBModel(login=user.login, password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def fill_info(db: AsyncSession, login: str, args: UserUpdateDBSchema):
    db_user = await get_user(db, login)
    for key, value in vars(args).items():
        if value is None:
            continue
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, login: str):
    result = await db.execute(select(UserDBModel).where(UserDBModel.login == login))
    return result.scalars().one_or_none()
