import json
from typing import Any

from methods.serializer_interface import SerializerInterface
from utils.timer import timer


class JsonSerializer(SerializerInterface):
    def __init__(self, cls):
        super().__init__("JSON", cls)

    @timer
    def serialize(self, input: Any, *args, **kwargs) -> Any:
        return json.dumps(input, *args, **kwargs).encode()

    @timer
    def deserialize(self, input: Any, *args, **kwargs) -> Any:
        return json.loads(input.decode(), *args, **kwargs)
