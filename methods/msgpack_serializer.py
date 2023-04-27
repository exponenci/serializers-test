import msgpack
from typing import Any

from serializer_interface import SerializerInterface
from utils.timer import timer


class MsgPackSerializer(SerializerInterface):
    def __init__(self, cls):
        super().__init__("MessagePack", cls)

    @timer
    def serialize(self, input: Any) -> Any:
        return msgpack.packb(input)

    @timer
    def deserialize(self, input: Any) -> Any:
        return msgpack.unpackb(input)
