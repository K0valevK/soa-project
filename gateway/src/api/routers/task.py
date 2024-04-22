import grpc
from aiokafka import AIOKafkaProducer
from api.routers.user import get_current_user
from config import settings
from fastapi import APIRouter, Depends, HTTPException, status
from google.protobuf.json_format import MessageToDict
from grpc_client import get_stub
from jose import jwt, JWTError
from schemas import Task, TaskCreate, TaskUpdate, User
from kafka_producer import get_kafka_producer, send_message
from typing import List

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
                                                    **task.model_dump())

    try:
        resp = await stub.CreateTask(task_req)
    except grpc.RpcError as rpc_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return Task(id=resp.task.id,
                creator_login=resp.task.creator_login,
                name=resp.task.name,
                text=resp.task.text)


@router.put("/{task_id}", response_model=Task)
async def upd_task(task_id: int,
                   args: TaskUpdate,
                   current_user: User = Depends(get_current_user),
                   stub: TaskManagerServerStub = Depends(get_stub)):
    task_req: UpdateTaskRequest = UpdateTaskRequest(id=task_id,
                                                    creator_login=current_user.login,
                                                    **args.model_dump())
    try:
        resp = await stub.UpdateTask(task_req)
    except grpc.RpcError as rpc_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return Task(id=resp.task.id,
                creator_login=resp.task.creator_login,
                name=resp.task.name,
                text=resp.task.text)


@router.delete("/{task_id}", response_model=Task)
async def delete_task(task_id: int,
                      current_user: User = Depends(get_current_user),
                      stub: TaskManagerServerStub = Depends(get_stub)):
    task_req: DeleteTaskRequest = DeleteTaskRequest(creator_login=current_user.login,
                                                    task_id=task_id)
    try:
        resp = await stub.DeleteTask(task_req)
    except grpc.RpcError as rpc_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return Task(id=resp.task.id,
                creator_login=resp.task.creator_login,
                name=resp.task.name,
                text=resp.task.text)


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int,
                   stub: TaskManagerServerStub = Depends(get_stub)):
    task_req: GetTaskRequest = GetTaskRequest(id=task_id)
    try:
        resp = await stub.GetTask(task_req)
    except grpc.RpcError as rpc_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return Task(id=resp.task.id,
                creator_login=resp.task.creator_login,
                name=resp.task.name,
                text=resp.task.text)


@router.get("", response_model=List[Task])
async def get_tasks_paginated(page: int,
                              limit: int,
                              stub: TaskManagerServerStub = Depends(get_stub)):
    if page < 0 or limit < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unacceptable argument")

    task_req: ListTasksRequest = ListTasksRequest(page=page, limit=limit)
    resp = await stub.ListTasks(task_req)
    result = [Task(**MessageToDict(i, preserving_proto_field_name=True)) for i in resp.tasks]

    return result


@router.get("/{task_id}/view")
async def view_task(task_id: int,
                    current_user: User = Depends(get_current_user),
                    stub: TaskManagerServerStub = Depends(get_stub),
                    producer: AIOKafkaProducer = Depends(get_kafka_producer)):
    task_req: GetTaskRequest = GetTaskRequest(id=task_id)
    try:
        resp = await stub.GetTask(task_req)
    except grpc.RpcError as rpc_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    await send_message(producer, settings.kafka_topic_views, {"user_login": current_user.login,
                                                              "task_id": task_id})


@router.get("/{task_id}/like")
async def like_task(task_id: int,
                    current_user: User = Depends(get_current_user),
                    stub: TaskManagerServerStub = Depends(get_stub),
                    producer: AIOKafkaProducer = Depends(get_kafka_producer)):
    task_req: GetTaskRequest = GetTaskRequest(id=task_id)
    try:
        resp = await stub.GetTask(task_req)
    except grpc.RpcError as rpc_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    await send_message(producer, settings.kafka_topic_likes, {"user_login": current_user.login,
                                                              "task_id": task_id})
