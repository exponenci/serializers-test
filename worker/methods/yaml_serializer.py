import yaml
from typing import Any

from methods.serializer_interface import SerializerInterface
from utils.timer import timer


class YamlSerializer(SerializerInterface):
    def __init__(self, container):
        super().__init__("YAML", container)

    @timer
    def serialize(self, input: Any, *args, **kwargs) -> Any:
        return yaml.dump(input, *args, **kwargs)

    @timer
    def deserialize(self, input: Any, *args, **kwargs) -> Any:
        return yaml.load(input, Loader=yaml.FullLoader, *args, **kwargs)
