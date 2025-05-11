from common import Common_pb2 as _Common_pb2
from common import Command_pb2 as _Command_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CLRMetricCollection(_message.Message):
    __slots__ = ("metrics", "service", "serviceInstance")
    METRICS_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    SERVICEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[CLRMetric]
    service: str
    serviceInstance: str
    def __init__(self, metrics: _Optional[_Iterable[_Union[CLRMetric, _Mapping]]] = ..., service: _Optional[str] = ..., serviceInstance: _Optional[str] = ...) -> None: ...

class CLRMetric(_message.Message):
    __slots__ = ("time", "cpu", "gc", "thread")
    TIME_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    GC_FIELD_NUMBER: _ClassVar[int]
    THREAD_FIELD_NUMBER: _ClassVar[int]
    time: int
    cpu: _Common_pb2.CPU
    gc: ClrGC
    thread: ClrThread
    def __init__(self, time: _Optional[int] = ..., cpu: _Optional[_Union[_Common_pb2.CPU, _Mapping]] = ..., gc: _Optional[_Union[ClrGC, _Mapping]] = ..., thread: _Optional[_Union[ClrThread, _Mapping]] = ...) -> None: ...

class ClrGC(_message.Message):
    __slots__ = ("Gen0CollectCount", "Gen1CollectCount", "Gen2CollectCount", "HeapMemory")
    GEN0COLLECTCOUNT_FIELD_NUMBER: _ClassVar[int]
    GEN1COLLECTCOUNT_FIELD_NUMBER: _ClassVar[int]
    GEN2COLLECTCOUNT_FIELD_NUMBER: _ClassVar[int]
    HEAPMEMORY_FIELD_NUMBER: _ClassVar[int]
    Gen0CollectCount: int
    Gen1CollectCount: int
    Gen2CollectCount: int
    HeapMemory: int
    def __init__(self, Gen0CollectCount: _Optional[int] = ..., Gen1CollectCount: _Optional[int] = ..., Gen2CollectCount: _Optional[int] = ..., HeapMemory: _Optional[int] = ...) -> None: ...

class ClrThread(_message.Message):
    __slots__ = ("AvailableCompletionPortThreads", "AvailableWorkerThreads", "MaxCompletionPortThreads", "MaxWorkerThreads")
    AVAILABLECOMPLETIONPORTTHREADS_FIELD_NUMBER: _ClassVar[int]
    AVAILABLEWORKERTHREADS_FIELD_NUMBER: _ClassVar[int]
    MAXCOMPLETIONPORTTHREADS_FIELD_NUMBER: _ClassVar[int]
    MAXWORKERTHREADS_FIELD_NUMBER: _ClassVar[int]
    AvailableCompletionPortThreads: int
    AvailableWorkerThreads: int
    MaxCompletionPortThreads: int
    MaxWorkerThreads: int
    def __init__(self, AvailableCompletionPortThreads: _Optional[int] = ..., AvailableWorkerThreads: _Optional[int] = ..., MaxCompletionPortThreads: _Optional[int] = ..., MaxWorkerThreads: _Optional[int] = ...) -> None: ...
