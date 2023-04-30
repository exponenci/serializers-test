from avro.io import DatumWriter, DatumReader, BinaryEncoder, BinaryDecoder
from io import BytesIO

from typing import Any

from methods.serializer_container.avro_container import AvroSerializerContainer
from methods.serializer_interface import SerializerInterface
from utils.timer import timer


class AvroSerializer(SerializerInterface):
    def __init__(self, container):
        if not isinstance(container, AvroSerializerContainer):
            raise AttributeError("invalid argument provided: container must be AvroSerializerContainer")
        super().__init__("Avro", container)

    @timer
    def serialize(self, input: Any, *args, **kwargs) -> Any:
        if self._container is None:
            return
        buffer = BytesIO()
        encoder = BinaryEncoder(buffer)
        self._writer = DatumWriter(self._container.get_schema())
        
        self._writer.write(input, encoder)
        return buffer.getvalue()

    @timer
    def deserialize(self, input: Any, *args, **kwargs) -> Any:
        if self._container is None:
            return
        buffer = BytesIO()
        buffer.write(input)
        buffer.seek(0)
        decoder = BinaryDecoder(buffer)
        self._reader = DatumReader(self._container.get_schema())
        return self._reader.read(decoder)
