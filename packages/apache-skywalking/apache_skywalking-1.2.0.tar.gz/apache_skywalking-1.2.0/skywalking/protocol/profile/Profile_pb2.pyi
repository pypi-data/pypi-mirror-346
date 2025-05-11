from common import Command_pb2 as _Command_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProfileTaskCommandQuery(_message.Message):
    __slots__ = ("service", "serviceInstance", "lastCommandTime")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    SERVICEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    LASTCOMMANDTIME_FIELD_NUMBER: _ClassVar[int]
    service: str
    serviceInstance: str
    lastCommandTime: int
    def __init__(self, service: _Optional[str] = ..., serviceInstance: _Optional[str] = ..., lastCommandTime: _Optional[int] = ...) -> None: ...

class ThreadSnapshot(_message.Message):
    __slots__ = ("taskId", "traceSegmentId", "time", "sequence", "stack")
    TASKID_FIELD_NUMBER: _ClassVar[int]
    TRACESEGMENTID_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    STACK_FIELD_NUMBER: _ClassVar[int]
    taskId: str
    traceSegmentId: str
    time: int
    sequence: int
    stack: ThreadStack
    def __init__(self, taskId: _Optional[str] = ..., traceSegmentId: _Optional[str] = ..., time: _Optional[int] = ..., sequence: _Optional[int] = ..., stack: _Optional[_Union[ThreadStack, _Mapping]] = ...) -> None: ...

class ThreadStack(_message.Message):
    __slots__ = ("codeSignatures",)
    CODESIGNATURES_FIELD_NUMBER: _ClassVar[int]
    codeSignatures: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, codeSignatures: _Optional[_Iterable[str]] = ...) -> None: ...

class ProfileTaskFinishReport(_message.Message):
    __slots__ = ("service", "serviceInstance", "taskId")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    SERVICEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    TASKID_FIELD_NUMBER: _ClassVar[int]
    service: str
    serviceInstance: str
    taskId: str
    def __init__(self, service: _Optional[str] = ..., serviceInstance: _Optional[str] = ..., taskId: _Optional[str] = ...) -> None: ...
