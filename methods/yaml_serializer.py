import yaml
from typing import Any

from serializer_interface import SerializerInterface
from utils.timer import timer


class YamlSerializer(SerializerInterface):
    def __init__(self, cls):
        super().__init__("YAML", cls)

    @timer
    def serialize(self, input: Any) -> Any:
        return yaml.dump(input)

    @timer
    def deserialize(self, input: Any) -> Any:
        return yaml.load(input, Loader=yaml.FullLoader)
