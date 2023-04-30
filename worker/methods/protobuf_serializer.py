from typing import Any

from methods.serializer_interface import SerializerInterface
from utils.timer import timer


class ProtobufSerializer(SerializerInterface):
    def __init__(self, container):
        super().__init__("Protobuf", container)
        if self._container is not None:
            self.instance = self._container.cls()
        else:
            self.instance = container.cls()

    @timer
    def serialize(self, input: Any, *args, **kwargs) -> Any:
        return input.SerializeToString()

    @timer
    def deserialize(self, input: Any, *args, **kwargs) -> Any:
        self.instance.ParseFromString(input)
        return self.instance
