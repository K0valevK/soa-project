# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: statistics.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10statistics.proto\x12\x0fstatistics_grpc\x1a\x1bgoogle/protobuf/empty.proto\"8\n\x04Task\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x14\n\x0c\x61uthor_login\x18\x02 \x01(\t\x12\x0e\n\x06metric\x18\x03 \x01(\x04\"$\n\x04User\x12\r\n\x05login\x18\x01 \x01(\t\x12\r\n\x05likes\x18\x02 \x01(\x04\"%\n\x12GetStatsOneRequest\x12\x0f\n\x07task_id\x18\x01 \x01(\x04\"L\n\x13GetStatsOneResponse\x12\x0f\n\x07task_id\x18\x01 \x01(\x04\x12\x11\n\tviews_num\x18\x02 \x01(\x04\x12\x11\n\tlikes_num\x18\x03 \x01(\x04\"\"\n\x12GetTopTasksRequest\x12\x0c\n\x04type\x18\x01 \x01(\t\";\n\x13GetTopTasksResponse\x12$\n\x05tasks\x18\x01 \x03(\x0b\x32\x15.statistics_grpc.Task\";\n\x13GetTopUsersResponse\x12$\n\x05users\x18\x01 \x03(\x0b\x32\x15.statistics_grpc.User2\x99\x02\n\x10StatisticsServer\x12Z\n\x0bGetStatsOne\x12#.statistics_grpc.GetStatsOneRequest\x1a$.statistics_grpc.GetStatsOneResponse\"\x00\x12Z\n\x0bGetTopTasks\x12#.statistics_grpc.GetTopTasksRequest\x1a$.statistics_grpc.GetTopTasksResponse\"\x00\x12M\n\x0bGetTopUsers\x12\x16.google.protobuf.Empty\x1a$.statistics_grpc.GetTopUsersResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'statistics_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_TASK']._serialized_start=66
  _globals['_TASK']._serialized_end=122
  _globals['_USER']._serialized_start=124
  _globals['_USER']._serialized_end=160
  _globals['_GETSTATSONEREQUEST']._serialized_start=162
  _globals['_GETSTATSONEREQUEST']._serialized_end=199
  _globals['_GETSTATSONERESPONSE']._serialized_start=201
  _globals['_GETSTATSONERESPONSE']._serialized_end=277
  _globals['_GETTOPTASKSREQUEST']._serialized_start=279
  _globals['_GETTOPTASKSREQUEST']._serialized_end=313
  _globals['_GETTOPTASKSRESPONSE']._serialized_start=315
  _globals['_GETTOPTASKSRESPONSE']._serialized_end=374
  _globals['_GETTOPUSERSRESPONSE']._serialized_start=376
  _globals['_GETTOPUSERSRESPONSE']._serialized_end=435
  _globals['_STATISTICSSERVER']._serialized_start=438
  _globals['_STATISTICSSERVER']._serialized_end=719
# @@protoc_insertion_point(module_scope)