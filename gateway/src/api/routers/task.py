from api.auth.oauth import oauth2_scheme, SECRET_KEY, ALGORITHM
from database import get_db_session
from grpc_client import get_stub
from schemas import Task, TaskCreate, TaskUpdate, User
from schemas.token import DataToken, Token
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt, JWTError
from api.routers.user import get_current_user
from typing import Annotated

from protos.task_manager_pb2_grpc import TaskManagerServerStub
from protos.task_manager_pb2 import CreateTaskRequest, UpdateTaskRequest, DeleteTaskRequest, GetTaskRequest, ListTasksRequest

router = APIRouter(
    prefix="/task",
    tags=["Tasks"],
)


@router.post("", response_model=Task)
async def new_task(task: TaskCreate,
                   current_user: User = Depends(get_current_user),
                   stub: TaskManagerServerStub = Depends(get_stub)):
    task_req: CreateTaskRequest = CreateTaskRequest(creator_login=current_user.login,
                                                    name=task.name,
                                                    text=task.text)

    resp = await stub.CreateTask(task_req)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code)
    return Task(id=resp.task.id,
                creator_login=resp.task.creator_login,
                name=resp.task.name,
                text=resp.task.text)


@router.put("/{task_name}", response_model=Task)
async def upd_task(task_name: str,
                   args: TaskUpdate,
                   current_user: User = Depends(get_current_user),
                   stub: TaskManagerServerStub = Depends(get_stub)):
    task_req: UpdateTaskRequest = UpdateTaskRequest(old_name=task_name,
                                                    creator_login=current_user.login,
                                                    **args.model_dump())
    resp = await stub.UpdateTask(task_req)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code)
    return Task(id=resp.task.id,
                creator_login=resp.task.creator_login,
                name=resp.task.name,
                text=resp.task.text)


@router.post("/{task_name}/close")
async def delete_task(task_name: str,
                      current_user: User = Depends(get_current_user),
                      stub: TaskManagerServerStub = Depends(get_stub)):
    task_req: DeleteTaskRequest = DeleteTaskRequest(creator_login=current_user.login,
                                                    name=task_name)
    resp = await stub.DeleteTask(task_req)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code)
    return 200


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int,
                   stub: TaskManagerServerStub = Depends(get_stub)):
    task_req: GetTaskRequest = GetTaskRequest(id=task_id)
    resp = await stub.GetTask(task_req)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code)
    return Task(id=resp.task.id,
                creator_login=resp.task.creator_login,
                name=resp.task.name,
                text=resp.task.text)


@router.get("")
async def get_tasks_paginated(page_toke: str,
                              stub: TaskManagerServerStub = Depends(get_stub)):
    pass
