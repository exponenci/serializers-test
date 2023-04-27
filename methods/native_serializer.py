from typing import Any

from serializer_interface import SerializerInterface
from utils.timer import timer


class NativeSerializer(SerializerInterface):
    def __init__(self, cls):
        super().__init__("Native", cls)

    @timer
    def serialize(self, input: Any) -> Any:
        return input.__str__()

    @timer
    def deserialize(self, input: Any) -> Any:
        return eval(input)
