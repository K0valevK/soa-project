from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateUserRequest(_message.Message):
    __slots__ = ("login",)
    LOGIN_FIELD_NUMBER: _ClassVar[int]
    login: str
    def __init__(self, login: _Optional[str] = ...) -> None: ...

class CreateUserResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class Task(_message.Message):
    __slots__ = ("id", "creator_login", "name", "text")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_LOGIN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    id: int
    creator_login: str
    name: str
    text: str
    def __init__(self, id: _Optional[int] = ..., creator_login: _Optional[str] = ..., name: _Optional[str] = ..., text: _Optional[str] = ...) -> None: ...

class CreateTaskRequest(_message.Message):
    __slots__ = ("creator_login", "name", "text")
    CREATOR_LOGIN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    creator_login: str
    name: str
    text: str
    def __init__(self, creator_login: _Optional[str] = ..., name: _Optional[str] = ..., text: _Optional[str] = ...) -> None: ...

class CreateTaskResponse(_message.Message):
    __slots__ = ("status_code", "task")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    task: Task
    def __init__(self, status_code: _Optional[int] = ..., task: _Optional[_Union[Task, _Mapping]] = ...) -> None: ...

class UpdateTaskRequest(_message.Message):
    __slots__ = ("old_name", "creator_login", "new_name", "text")
    OLD_NAME_FIELD_NUMBER: _ClassVar[int]
    CREATOR_LOGIN_FIELD_NUMBER: _ClassVar[int]
    NEW_NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    old_name: str
    creator_login: str
    new_name: str
    text: str
    def __init__(self, old_name: _Optional[str] = ..., creator_login: _Optional[str] = ..., new_name: _Optional[str] = ..., text: _Optional[str] = ...) -> None: ...

class UpdateTaskResponse(_message.Message):
    __slots__ = ("status_code", "task")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    task: Task
    def __init__(self, status_code: _Optional[int] = ..., task: _Optional[_Union[Task, _Mapping]] = ...) -> None: ...

class DeleteTaskRequest(_message.Message):
    __slots__ = ("creator_login", "name")
    CREATOR_LOGIN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    creator_login: str
    name: str
    def __init__(self, creator_login: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class DeleteTaskResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class GetTaskRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GetTaskResponse(_message.Message):
    __slots__ = ("status_code", "task")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    task: Task
    def __init__(self, status_code: _Optional[int] = ..., task: _Optional[_Union[Task, _Mapping]] = ...) -> None: ...

class ListTasksRequest(_message.Message):
    __slots__ = ("page", "limit")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    page: int
    limit: int
    def __init__(self, page: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class ListTasksResponse(_message.Message):
    __slots__ = ("status_code", "tasks")
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    TASKS_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    tasks: _containers.RepeatedCompositeFieldContainer[Task]
    def __init__(self, status_code: _Optional[int] = ..., tasks: _Optional[_Iterable[_Union[Task, _Mapping]]] = ...) -> None: ...
