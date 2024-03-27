from database import sessionmanager
from models import User as UserDBModel
from schemas import UserCreate as UserCreateDBSchema
from sqlalchemy.ext.asyncio import AsyncSession
from utils import thread_return, thread_lock, func_mapped


async def create_user(user: UserCreateDBSchema):
    async with sessionmanager.session() as db:
        db_user = UserDBModel(**user.model_dump())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
    with thread_lock[func_mapped['CreateUser']]:
        thread_return[func_mapped['CreateUser']] = 200
    return db_user
