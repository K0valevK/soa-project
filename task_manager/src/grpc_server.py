from concurrent import futures
from crud.task import create_task, fill_task_info, delete_task, get_task_by_id, get_tasks_paginated
from crud.user import create_user
from schemas import UserCreate, TaskCreate, TaskUpdate
from protos import task_manager_pb2, task_manager_pb2_grpc

import grpc


class TaskManagerServer(task_manager_pb2_grpc.TaskManagerServerServicer):
    async def CreateUser(self, request, context):
        result = await create_user(UserCreate(login=request.login))
        return task_manager_pb2.CreateUserResponse(user=task_manager_pb2.User(**result.model_dump()))

    async def CreateTask(self, request, context):
        task: TaskCreate = TaskCreate(creator_login=request.creator_login,
                                      name=request.name,
                                      text=request.text)

        result = await create_task(task)

        ret_task = task_manager_pb2.Task(**result.model_dump())

        return task_manager_pb2.CreateTaskResponse(task=ret_task)

    async def UpdateTask(self, request, context):
        task: TaskUpdate = TaskUpdate(name=request.new_name,
                                      text=request.text)
        if task.name == '':
            task.name = None
        if task.text == '':
            task.text = None

        result = await fill_task_info(request.id, request.creator_login, task)
        if result is not None:
            ret_task = task_manager_pb2.Task(**result.model_dump())
        else:
            ret_task = task_manager_pb2.Task()
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Task not found")

        return task_manager_pb2.UpdateTaskResponse(task=ret_task)

    async def DeleteTask(self, request, context):
        result = await delete_task(request.creator_login, request.task_id)
        if result is None:
            ret_task = task_manager_pb2.Task()
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Task not found")
        else:
            ret_task = task_manager_pb2.Task(**result.model_dump())

        return task_manager_pb2.DeleteTaskResponse(task=ret_task)

    async def GetTask(self, request, context):
        result = await get_task_by_id(request.id)
        if result is not None:
            ret_task = task_manager_pb2.Task(**result.model_dump())
        else:
            ret_task = task_manager_pb2.Task()
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Task not found")
        return task_manager_pb2.GetTaskResponse(task=ret_task)

    async def ListTasks(self, request, context):
        result = await get_tasks_paginated(request.page, request.limit)
        ret_tasks = [task_manager_pb2.Task(**i.model_dump()) for i in result]
        return task_manager_pb2.ListTasksResponse(tasks=ret_tasks)


server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
task_manager_pb2_grpc.add_TaskManagerServerServicer_to_server(TaskManagerServer(), server)
