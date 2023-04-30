from typing import Any

from methods.serializer_interface import SerializerInterface
from utils.timer import timer


class NativeSerializer(SerializerInterface):
    def __init__(self, container):
        super().__init__("Native", container)

    @timer
    def serialize(self, input: Any, *args, **kwargs) -> Any:
        return input.__str__().encode()

    @timer
    def deserialize(self, input: Any, *args, **kwargs) -> Any:
        return eval(input.decode())
