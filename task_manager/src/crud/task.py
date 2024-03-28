from database import sessionmanager
from models import Task as TaskDBModel
from models.task import toTaskSchema
from schemas import TaskCreate as TaskCreateDBSchema
from schemas import TaskUpdate as TaskUpdateDBSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_task(task: TaskCreateDBSchema):
    async with sessionmanager.session() as db:
        tmp_task = await get_task_by_name(db, task.creator_login, task.name)
        if tmp_task is not None:
            return 400, None

        db_task = TaskDBModel(**task.model_dump())
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)

    return 200, toTaskSchema(db_task)


async def fill_task_info(task_name: str, creator_login: str, args: TaskUpdateDBSchema):
    async with sessionmanager.session() as db:
        db_task = await get_task_by_name(db, creator_login, task_name)
        if db_task is None:
            return 404, None

        for key, value in vars(args).items():
            if value is None:
                continue
            setattr(db_task, key, value)
        await db.commit()
        await db.refresh(db_task)

    return 200, toTaskSchema(db_task)


async def get_task_by_id(task_id: int):
    async with sessionmanager.session() as db:
        result = (await db.execute(select(TaskDBModel).where(TaskDBModel.id == task_id))).scalars().one_or_none()
    if result is None:
        return 404, None
    return 200, toTaskSchema(result)


async def delete_task(creator_login: str, task_name: str):
    async with sessionmanager.session() as db:
        db_task = await get_task_by_name(db, creator_login, task_name)
        if db_task is None:
            return 404

        await db.delete(db_task)
        await db.commit()
    return 200


async def get_tasks_paginated(page: int, limit: int):
    async with sessionmanager.session() as db:
        result = (await db.execute(select(TaskDBModel).where(TaskDBModel.id > page * limit).limit(limit))).scalars().all()
    return 200, list(map(toTaskSchema, result))


async def get_task_by_name(db: AsyncSession, creator_login: str, task_name: str):
    result = await db.execute(select(TaskDBModel).where(TaskDBModel.creator_login == creator_login,
                                                        TaskDBModel.name == task_name))
    return result.scalars().one_or_none()
