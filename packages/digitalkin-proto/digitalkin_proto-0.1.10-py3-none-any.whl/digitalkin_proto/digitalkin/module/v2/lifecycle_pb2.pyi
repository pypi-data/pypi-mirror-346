from buf.validate import validate_pb2 as _validate_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StartModuleRequest(_message.Message):
    __slots__ = ("input", "setup_id", "mission_id")
    INPUT_FIELD_NUMBER: _ClassVar[int]
    SETUP_ID_FIELD_NUMBER: _ClassVar[int]
    MISSION_ID_FIELD_NUMBER: _ClassVar[int]
    input: _struct_pb2.Struct
    setup_id: str
    mission_id: str
    def __init__(self, input: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., setup_id: _Optional[str] = ..., mission_id: _Optional[str] = ...) -> None: ...

class StopModuleRequest(_message.Message):
    __slots__ = ("job_id",)
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class StartModuleResponse(_message.Message):
    __slots__ = ("success", "output", "job_id")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    success: bool
    output: _struct_pb2.Struct
    job_id: str
    def __init__(self, success: bool = ..., output: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., job_id: _Optional[str] = ...) -> None: ...

class StopModuleResponse(_message.Message):
    __slots__ = ("success", "job_id")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    success: bool
    job_id: str
    def __init__(self, success: bool = ..., job_id: _Optional[str] = ...) -> None: ...
