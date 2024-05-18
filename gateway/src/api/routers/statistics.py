import grpc
from config import settings
from fastapi import APIRouter, Depends, HTTPException, status
from google.protobuf.json_format import MessageToDict
from grpc_client import get_stats_stub
from jose import jwt, JWTError
from typing import List

from protos.statistics_pb2_grpc import StatisticsServerStub
from protos.statistics_pb2 import GetStatsOneRequest, GetTopTasksRequest, google_dot_protobuf_dot_empty__pb2


router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"],
)


@router.get("/{task_id}")
async def task_stats(task_id: int,
                     stub: StatisticsServerStub = Depends(get_stats_stub)):
    # TODO: Foolproof request
    stats_req: GetStatsOneRequest = GetStatsOneRequest(task_id=task_id)

    try:
        resp = await stub.GetStatsOne(stats_req)
    except grpc.RpcError as rpc_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return {"task_id": resp.task_id, "views_num": resp.views_num, "likes_num": resp.likes_num}


@router.get("/tasks/{metric_type}")
async def top_tasks(metric_type: str,
                    stub: StatisticsServerStub = Depends(get_stats_stub)):
    if metric_type not in ["likes", "views"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    stats_req: GetTopTasksRequest = GetTopTasksRequest(type=metric_type)

    resp = await stub.GetTopTasks(stats_req)
    result = [MessageToDict(i, preserving_proto_field_name=True) for i in resp.tasks]

    return result


@router.get("/users/top")
async def top_users(stub: StatisticsServerStub = Depends(get_stats_stub)):
    resp = await stub.GetTopUsers(google_dot_protobuf_dot_empty__pb2.Empty())
    result = [MessageToDict(i, preserving_proto_field_name=True) for i in resp.users]

    return result
