from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImageYUV444(_message.Message):
    __slots__ = ("header", "width", "height", "y_plane", "u_plane", "v_plane")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    Y_PLANE_FIELD_NUMBER: _ClassVar[int]
    U_PLANE_FIELD_NUMBER: _ClassVar[int]
    V_PLANE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    width: int
    height: int
    y_plane: bytes
    u_plane: bytes
    v_plane: bytes
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., y_plane: _Optional[bytes] = ..., u_plane: _Optional[bytes] = ..., v_plane: _Optional[bytes] = ...) -> None: ...
