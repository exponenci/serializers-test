from typing import Any

from methods.serializer_container.proto_container import ProtoSerializerContainer
from methods.serializer_interface import SerializerInterface
from utils.timer import timer


class ProtobufSerializer(SerializerInterface):
    def __init__(self, container):
        super().__init__("Protobuf", container)
        if not isinstance(container, ProtoSerializerContainer):
            raise AttributeError("invalid argument provided: container must be ProtoSerializerContainer")
        elif self._container is not None:
            self.instance = self._container.cls()

    @timer
    def serialize(self, input: Any, *args, **kwargs) -> Any:
        return input.SerializeToString()

    @timer
    def deserialize(self, input: Any, *args, **kwargs) -> Any:
        self.instance.ParseFromString(input)
        return self.instance
