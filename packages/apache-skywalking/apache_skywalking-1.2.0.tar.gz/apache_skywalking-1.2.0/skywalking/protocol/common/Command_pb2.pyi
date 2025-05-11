from common import Common_pb2 as _Common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Command(_message.Message):
    __slots__ = ("command", "args")
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    command: str
    args: _containers.RepeatedCompositeFieldContainer[_Common_pb2.KeyStringValuePair]
    def __init__(self, command: _Optional[str] = ..., args: _Optional[_Iterable[_Union[_Common_pb2.KeyStringValuePair, _Mapping]]] = ...) -> None: ...

class Commands(_message.Message):
    __slots__ = ("commands",)
    COMMANDS_FIELD_NUMBER: _ClassVar[int]
    commands: _containers.RepeatedCompositeFieldContainer[Command]
    def __init__(self, commands: _Optional[_Iterable[_Union[Command, _Mapping]]] = ...) -> None: ...
