from concurrent import futures
from crud.statistics import task_stats, top_tasks, top_users
from protos import statistics_pb2, statistics_pb2_grpc

import grpc


class StatisticsServer(statistics_pb2_grpc.StatisticsServerServicer):
    async def GetStatsOne(self, request, context):
        result = await task_stats(request.task_id)
        return statistics_pb2.GetStatsOneResponse(task_id=request.task_id, **result)

    async def GetTopTasks(self, request, context):
        result = await top_tasks(request.type)
        ret_tasks = [statistics_pb2.Task(id=result[i][0],
                                         author_login=result[i][1],
                                         metric=result[i][2]) for i in range(len(result))]

        return statistics_pb2.GetTopTasksResponse(tasks=ret_tasks)

    async def GetTopUsers(self, request, context):
        result = await top_users()
        ret_users = [statistics_pb2.User(login=result[i][0],
                                         likes=result[i][1]) for i in range(len(result))]

        return statistics_pb2.GetTopUsersResponse(users=ret_users)


server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
statistics_pb2_grpc.add_StatisticsServerServicer_to_server(StatisticsServer(), server)
