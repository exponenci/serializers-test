import sys
from typing import Any

from utils.timer import timer


class SerializerInterface:
    def __init__(self, method_name: str, cls):
        self._method_name: str = method_name
        self._cls = cls

    def method_name(self) -> str:
        return self._method_name

    def cls_size(self) -> int:
        serialized_object, _ = self.serialize(self._cls())
        return sys.getsizeof(serialized_object)

    @timer
    def serialize(self, input: Any) -> Any:
        SerializerInterface._pure_virtual_func()

    @timer
    def deserialize(self, input: Any) -> Any:
        SerializerInterface._pure_virtual_func()

    def run_experiment(self, run_count: int = 1000):
        serialization_time_sum, deserialization_time_sum = 0, 0
        
        for _ in range(run_count):
            seriazlized_object, time = self.serialize(self._cls())
            serialization_time_sum += time

            _, time = self.deserialize(seriazlized_object)
            deserialization_time_sum += time
        
        mean_ser_time = serialization_time_sum / run_count
        mean_deser_time = deserialization_time_sum / run_count
        return mean_ser_time, mean_deser_time
    
    def run_and_print_experiment(self, *args, **kwargs):
        mean_ser_time, mean_deser_time = self.run_experiment(*args, **kwargs)
        return "{}-{}-{}ms-{}ms".format(
            self.method_name(), 
            self.cls_size(), 
            mean_ser_time * 1e6, 
            mean_deser_time * 1e6)

    @staticmethod
    def _pure_virtual_func():
        raise RuntimeError("SerializerInterface: virtual function is not defined")
