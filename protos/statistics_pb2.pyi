from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Task(_message.Message):
    __slots__ = ("id", "author_login", "metric")
    ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_LOGIN_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    id: int
    author_login: str
    metric: int
    def __init__(self, id: _Optional[int] = ..., author_login: _Optional[str] = ..., metric: _Optional[int] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("login", "likes")
    LOGIN_FIELD_NUMBER: _ClassVar[int]
    LIKES_FIELD_NUMBER: _ClassVar[int]
    login: str
    likes: int
    def __init__(self, login: _Optional[str] = ..., likes: _Optional[int] = ...) -> None: ...

class GetStatsOneRequest(_message.Message):
    __slots__ = ("task_id",)
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    def __init__(self, task_id: _Optional[int] = ...) -> None: ...

class GetStatsOneResponse(_message.Message):
    __slots__ = ("task_id", "views_num", "likes_num")
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    VIEWS_NUM_FIELD_NUMBER: _ClassVar[int]
    LIKES_NUM_FIELD_NUMBER: _ClassVar[int]
    task_id: int
    views_num: int
    likes_num: int
    def __init__(self, task_id: _Optional[int] = ..., views_num: _Optional[int] = ..., likes_num: _Optional[int] = ...) -> None: ...

class GetTopTasksRequest(_message.Message):
    __slots__ = ("type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: str
    def __init__(self, type: _Optional[str] = ...) -> None: ...

class GetTopTasksResponse(_message.Message):
    __slots__ = ("tasks",)
    TASKS_FIELD_NUMBER: _ClassVar[int]
    tasks: _containers.RepeatedCompositeFieldContainer[Task]
    def __init__(self, tasks: _Optional[_Iterable[_Union[Task, _Mapping]]] = ...) -> None: ...

class GetTopUsersResponse(_message.Message):
    __slots__ = ("users",)
    USERS_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(self, users: _Optional[_Iterable[_Union[User, _Mapping]]] = ...) -> None: ...
