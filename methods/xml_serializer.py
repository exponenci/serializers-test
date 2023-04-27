import xmltodict
import dicttoxml
from typing import Any

from serializer_interface import SerializerInterface
from utils.timer import timer


class XmlSerializer(SerializerInterface):
    def __init__(self, cls):
        super().__init__("XML", cls)

    @timer
    def serialize(self, input: Any) -> Any:
        return dicttoxml.dicttoxml(input)

    @timer
    def deserialize(self, input: Any) -> Any:
        return xmltodict.parse(input)
