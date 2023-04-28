from typing import Any

from serializer_interface import SerializerInterface
from utils.timer import timer


class ProtobufSerializer(SerializerInterface):
    def __init__(self, container):
        super().__init__("protobuf", container)

    @timer
    def serialize(self, input: Any, *args, **kwargs) -> Any:
        return input.SerializeToString()

    @timer
    def deserialize(self, input: Any, *args, **kwargs) -> Any:
        if self._container is None:
            return
        instance = self._container.cls()
        instance.ParseFromString(input)
        return instance
