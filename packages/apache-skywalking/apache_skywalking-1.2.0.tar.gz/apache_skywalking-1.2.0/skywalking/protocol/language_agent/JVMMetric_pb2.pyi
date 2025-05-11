from common import Common_pb2 as _Common_pb2
from common import Command_pb2 as _Command_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PoolType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CODE_CACHE_USAGE: _ClassVar[PoolType]
    NEWGEN_USAGE: _ClassVar[PoolType]
    OLDGEN_USAGE: _ClassVar[PoolType]
    SURVIVOR_USAGE: _ClassVar[PoolType]
    PERMGEN_USAGE: _ClassVar[PoolType]
    METASPACE_USAGE: _ClassVar[PoolType]
    ZHEAP_USAGE: _ClassVar[PoolType]
    COMPRESSED_CLASS_SPACE_USAGE: _ClassVar[PoolType]
    CODEHEAP_NON_NMETHODS_USAGE: _ClassVar[PoolType]
    CODEHEAP_PROFILED_NMETHODS_USAGE: _ClassVar[PoolType]
    CODEHEAP_NON_PROFILED_NMETHODS_USAGE: _ClassVar[PoolType]

class GCPhase(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NEW: _ClassVar[GCPhase]
    OLD: _ClassVar[GCPhase]
    NORMAL: _ClassVar[GCPhase]
CODE_CACHE_USAGE: PoolType
NEWGEN_USAGE: PoolType
OLDGEN_USAGE: PoolType
SURVIVOR_USAGE: PoolType
PERMGEN_USAGE: PoolType
METASPACE_USAGE: PoolType
ZHEAP_USAGE: PoolType
COMPRESSED_CLASS_SPACE_USAGE: PoolType
CODEHEAP_NON_NMETHODS_USAGE: PoolType
CODEHEAP_PROFILED_NMETHODS_USAGE: PoolType
CODEHEAP_NON_PROFILED_NMETHODS_USAGE: PoolType
NEW: GCPhase
OLD: GCPhase
NORMAL: GCPhase

class JVMMetricCollection(_message.Message):
    __slots__ = ("metrics", "service", "serviceInstance")
    METRICS_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    SERVICEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[JVMMetric]
    service: str
    serviceInstance: str
    def __init__(self, metrics: _Optional[_Iterable[_Union[JVMMetric, _Mapping]]] = ..., service: _Optional[str] = ..., serviceInstance: _Optional[str] = ...) -> None: ...

class JVMMetric(_message.Message):
    __slots__ = ("time", "cpu", "memory", "memoryPool", "gc", "thread", "clazz")
    TIME_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    MEMORYPOOL_FIELD_NUMBER: _ClassVar[int]
    GC_FIELD_NUMBER: _ClassVar[int]
    THREAD_FIELD_NUMBER: _ClassVar[int]
    CLAZZ_FIELD_NUMBER: _ClassVar[int]
    time: int
    cpu: _Common_pb2.CPU
    memory: _containers.RepeatedCompositeFieldContainer[Memory]
    memoryPool: _containers.RepeatedCompositeFieldContainer[MemoryPool]
    gc: _containers.RepeatedCompositeFieldContainer[GC]
    thread: Thread
    clazz: Class
    def __init__(self, time: _Optional[int] = ..., cpu: _Optional[_Union[_Common_pb2.CPU, _Mapping]] = ..., memory: _Optional[_Iterable[_Union[Memory, _Mapping]]] = ..., memoryPool: _Optional[_Iterable[_Union[MemoryPool, _Mapping]]] = ..., gc: _Optional[_Iterable[_Union[GC, _Mapping]]] = ..., thread: _Optional[_Union[Thread, _Mapping]] = ..., clazz: _Optional[_Union[Class, _Mapping]] = ...) -> None: ...

class Memory(_message.Message):
    __slots__ = ("isHeap", "init", "max", "used", "committed")
    ISHEAP_FIELD_NUMBER: _ClassVar[int]
    INIT_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    USED_FIELD_NUMBER: _ClassVar[int]
    COMMITTED_FIELD_NUMBER: _ClassVar[int]
    isHeap: bool
    init: int
    max: int
    used: int
    committed: int
    def __init__(self, isHeap: bool = ..., init: _Optional[int] = ..., max: _Optional[int] = ..., used: _Optional[int] = ..., committed: _Optional[int] = ...) -> None: ...

class MemoryPool(_message.Message):
    __slots__ = ("type", "init", "max", "used", "committed")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INIT_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    USED_FIELD_NUMBER: _ClassVar[int]
    COMMITTED_FIELD_NUMBER: _ClassVar[int]
    type: PoolType
    init: int
    max: int
    used: int
    committed: int
    def __init__(self, type: _Optional[_Union[PoolType, str]] = ..., init: _Optional[int] = ..., max: _Optional[int] = ..., used: _Optional[int] = ..., committed: _Optional[int] = ...) -> None: ...

class GC(_message.Message):
    __slots__ = ("phase", "count", "time")
    PHASE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    phase: GCPhase
    count: int
    time: int
    def __init__(self, phase: _Optional[_Union[GCPhase, str]] = ..., count: _Optional[int] = ..., time: _Optional[int] = ...) -> None: ...

class Thread(_message.Message):
    __slots__ = ("liveCount", "daemonCount", "peakCount", "runnableStateThreadCount", "blockedStateThreadCount", "waitingStateThreadCount", "timedWaitingStateThreadCount")
    LIVECOUNT_FIELD_NUMBER: _ClassVar[int]
    DAEMONCOUNT_FIELD_NUMBER: _ClassVar[int]
    PEAKCOUNT_FIELD_NUMBER: _ClassVar[int]
    RUNNABLESTATETHREADCOUNT_FIELD_NUMBER: _ClassVar[int]
    BLOCKEDSTATETHREADCOUNT_FIELD_NUMBER: _ClassVar[int]
    WAITINGSTATETHREADCOUNT_FIELD_NUMBER: _ClassVar[int]
    TIMEDWAITINGSTATETHREADCOUNT_FIELD_NUMBER: _ClassVar[int]
    liveCount: int
    daemonCount: int
    peakCount: int
    runnableStateThreadCount: int
    blockedStateThreadCount: int
    waitingStateThreadCount: int
    timedWaitingStateThreadCount: int
    def __init__(self, liveCount: _Optional[int] = ..., daemonCount: _Optional[int] = ..., peakCount: _Optional[int] = ..., runnableStateThreadCount: _Optional[int] = ..., blockedStateThreadCount: _Optional[int] = ..., waitingStateThreadCount: _Optional[int] = ..., timedWaitingStateThreadCount: _Optional[int] = ...) -> None: ...

class Class(_message.Message):
    __slots__ = ("loadedClassCount", "totalUnloadedClassCount", "totalLoadedClassCount")
    LOADEDCLASSCOUNT_FIELD_NUMBER: _ClassVar[int]
    TOTALUNLOADEDCLASSCOUNT_FIELD_NUMBER: _ClassVar[int]
    TOTALLOADEDCLASSCOUNT_FIELD_NUMBER: _ClassVar[int]
    loadedClassCount: int
    totalUnloadedClassCount: int
    totalLoadedClassCount: int
    def __init__(self, loadedClassCount: _Optional[int] = ..., totalUnloadedClassCount: _Optional[int] = ..., totalLoadedClassCount: _Optional[int] = ...) -> None: ...
