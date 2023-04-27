import json
from typing import Any

from serializer_interface import SerializerInterface
from utils.timer import timer


class JsonSerializer(SerializerInterface):
    def __init__(self, cls):
        super().__init__("JSON", cls)

    @timer
    def serialize(self, input: Any) -> Any:
        return json.dumps(input)

    @timer
    def deserialize(self, input: Any) -> Any:
        return json.loads(input)
