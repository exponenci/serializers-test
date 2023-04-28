from abc import abstractmethod, ABC
from typing import Any

from utils.timer import timer


class SerializerInterface(ABC):
    def __init__(self, method_name: str = '', container=None):
        self._method_name: str = method_name
        self._container = container

    def method_name(self) -> str:
        return self._method_name

    @abstractmethod
    @timer
    def serialize(self, input: Any, *args, **kwargs) -> Any:
        SerializerInterface._pure_virtual_func()

    @abstractmethod
    @timer
    def deserialize(self, input: Any, *args, **kwargs) -> Any:
        SerializerInterface._pure_virtual_func()


    @staticmethod
    def _pure_virtual_func():
        raise RuntimeError("SerializerInterface: virtual function is not defined")
