import xmltodict
from typing import Any

from serializer_interface import SerializerInterface
from utils.timer import timer


class XmlSerializer(SerializerInterface):
    def __init__(self, container):
        super().__init__("XML", container)

    @timer
    def serialize(self, input: Any, *args, **kwargs) -> Any:
        return xmltodict.unparse(input, *args, **kwargs)

    @timer
    def deserialize(self, input: Any, *args, **kwargs) -> Any:
        return xmltodict.parse(input, *args, **kwargs)
