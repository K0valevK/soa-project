from database import sessionmanager
from models import Task as TaskDBModel
from models.task import toTaskSchema
from schemas import TaskCreate as TaskCreateDBSchema
from schemas import TaskUpdate as TaskUpdateDBSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_task(task: TaskCreateDBSchema):
    async with sessionmanager.session() as db:
        db_task = TaskDBModel(**task.model_dump())
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)

    return toTaskSchema(db_task)


async def fill_task_info(task_name: str, creator_login: str, args: TaskUpdateDBSchema):
    async with sessionmanager.session() as db:
        db_task = await get_task_by_name(db, creator_login, task_name)
        for key, value in vars(args).items():
            if value is None:
                continue
            setattr(db_task, key, value)
        await db.commit()
        await db.refresh(db_task)

    return toTaskSchema(db_task)


async def get_task_by_id(task_id: int):
    async with sessionmanager.session() as db:
        result = (await db.execute(select(TaskDBModel).where(TaskDBModel.id == task_id))).scalars().one_or_none()
    return toTaskSchema(result)


async def delete_task(creator_login: str, task_name: str):
    async with sessionmanager.session() as db:
        db_task = await get_task_by_name(db, creator_login, task_name)
        await db.delete(db_task)
        await db.commit()
    return 200


async def get_task_by_name(db: AsyncSession, creator_login: str, task_name: str):
    cond = TaskDBModel.creator_login == creator_login and TaskDBModel.name == task_name
    result = await db.execute(select(TaskDBModel).where(cond))
    return result.scalars().one_or_none()
