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


async def fill_task_info(task_id: int, creator_login: str, args: TaskUpdateDBSchema):
    async with sessionmanager.session() as db:
        db_task = await get_task_by_id_locked(db, creator_login, task_id)
        if db_task is None:
            return None

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
    if result is None:
        return None
    return toTaskSchema(result)


async def delete_task(creator_login: str, task_id: int):
    async with sessionmanager.session() as db:
        db_task = await get_task_by_id_locked(db, creator_login, task_id)
        if db_task is None:
            return None

        await db.delete(db_task)
        await db.commit()
    return toTaskSchema(db_task)


async def get_tasks_paginated(page: int, limit: int):
    async with sessionmanager.session() as db:
        result = (await db.execute(select(TaskDBModel).where(TaskDBModel.id > page * limit).limit(limit))).scalars().all()
    return list(map(toTaskSchema, result))


async def get_task_by_id_locked(db: AsyncSession, creator_login: str, task_id: int):
    result = await db.execute(select(TaskDBModel).where(TaskDBModel.creator_login == creator_login,
                                                        TaskDBModel.id == task_id))
    return result.scalars().one_or_none()
