import grpc
import protos.task_manager_pb2_grpc

from concurrent import futures
from crud.task import create_task, fill_task_info, delete_task, get_task_by_id
from crud.user import create_user
from schemas import UserCreate, TaskCreate, TaskUpdate
from protos.task_manager_pb2 import CreateUserResponse, CreateTaskResponse, UpdateTaskResponse, DeleteTaskResponse, GetTaskResponse, Task


class TaskManagerServerService(protos.task_manager_pb2_grpc.TaskManagerServerServicer):
    async def CreateUser(self, request, context):
        result = await create_user(UserCreate(login=request.login))
        return CreateUserResponse(status_code=result)

    async def CreateTask(self, request, context):
        task: TaskCreate = TaskCreate(creator_login=request.creator_login,
                                      name=request.name,
                                      text=request.text)

        # result = run_and_return(create_task, 'CreateTask', task)
        result = await create_task(task)

        if result[0] == 200:
            ret_task = Task(**result[1].model_dump())
        else:
            ret_task = Task()

        return CreateTaskResponse(status_code=result[0],
                                  task=ret_task)

    async def UpdateTask(self, request, context):
        task: TaskUpdate = TaskUpdate(name=request.new_name,
                                      text=request.text)
        if task.name == '':
            task.name = None
        if task.text == '':
            task.text = None

        result = await fill_task_info(request.old_name, request.creator_login, task)
        if result[0] == 200:
            ret_task = Task(**result[1].model_dump())
        else:
            ret_task = Task()

        return UpdateTaskResponse(status_code=result[0],
                                  task=ret_task)

    async def DeleteTask(self, request, context):
        result = await delete_task(request.creator_login, request.name)
        return DeleteTaskResponse(status_code=result)

    async def GetTask(self, request, context):
        result = await get_task_by_id(request.id)
        if result[0] == 200:
            ret_task = Task(**result[1].model_dump())
        else:
            ret_task = Task()
        return GetTaskResponse(status_code=result[0], task=ret_task)


server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
protos.task_manager_pb2_grpc.add_TaskManagerServerServicer_to_server(TaskManagerServerService(), server)
