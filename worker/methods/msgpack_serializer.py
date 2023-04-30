import msgpack
from typing import Any

from methods.serializer_interface import SerializerInterface
from utils.timer import timer


class MsgPackSerializer(SerializerInterface):
    def __init__(self, cls):
        super().__init__("MessagePack", cls)

    @timer
    def serialize(self, input: Any, *args, **kwargs) -> Any:
        return msgpack.packb(input, *args, **kwargs)

    @timer
    def deserialize(self, input: Any, *args, **kwargs) -> Any:
        return msgpack.unpackb(input, *args, **kwargs)
