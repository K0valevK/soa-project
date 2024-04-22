from database import sessionmanager
from models import User as UserDBModel
from models.user import toUserSchema
from schemas import UserCreate as UserCreateDBSchema
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(user: UserCreateDBSchema):
    async with sessionmanager.session() as db:
        db_user = UserDBModel(**user.model_dump())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
    return toUserSchema(db_user)
