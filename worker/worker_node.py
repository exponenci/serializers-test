import os
import sys
import socket
import struct

from typing import Any, Union

from methods import AvroSerializer, JsonSerializer, \
    MsgPackSerializer, NativeSerializer, \
    XmlSerializer, YamlSerializer, \
    ProtobufSerializer, SerializerInterface

from methods.serializer_container.base_container import BaseSerializerContainer


def get_env_values(*args):
    result = list()
    for arg in args:
        result.append(os.getenv(arg))
    return result


def get_serializer(method_name: str, *args):
    method_name = method_name.lower()
    if method_name == "native":
        return NativeSerializer(*args)
    elif method_name == "xml":
        return XmlSerializer(*args)
    elif method_name == "json":
        return JsonSerializer(*args)
    elif method_name.find("proto") != -1:
        return ProtobufSerializer(*args)
    elif method_name.find("avro") != -1:
        return AvroSerializer(*args)
    elif method_name == "yaml":
        return YamlSerializer(*args)
    elif method_name == "msgpack" or method_name == "messagepack":
        return MsgPackSerializer(*args)
    else:
        raise NameError("No such serialization method found!")


def get_container(method_name: str):
    from experiment_meta.pydict import datastruct_dict
    if method_name.find("avro") != -1:
        from methods.serializer_container.avro_container import AvroSerializerContainer
        from experiment_meta.avro import datastruct_avro_scheme
        return AvroSerializerContainer(datastruct_dict, datastruct_avro_scheme)
    elif method_name.find("proto") != -1:
        from methods.serializer_container.proto_container import ProtoSerializerContainer
        from experiment_meta.datastruct_pb2 import DataStruct
        return ProtoSerializerContainer(datastruct_dict, DataStruct)
    else:
        return BaseSerializerContainer(datastruct_dict)


class Worker:
    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.container: Any = None
        self.serializer: Union[SerializerInterface, None] = None

    def set_serializer(self, method_name: str = 'native'):
        self.container = get_container(method_name)
        self.serializer = get_serializer(method_name, self.container)
        return self

    def set_udp_settings(self, addr: str = 'localhost', port: int = 9889):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((addr, port))
        mreq = struct.pack("4sl", socket.inet_aton(addr), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        return self

    def loop(self):
        while True:
            request, request_addr = self.sock.recvfrom(32 * 1024)
            # get_json(request)
            result = self.format_experiment_result(*self.run_experiment())
            self.sock.sendto(result.encode(), request_addr)

    def run_experiment(self, run_count: int = 1000):
        if self.serializer is None:
            return -1, -1
        serialization_time_sum, deserialization_time_sum = 0, 0
        
        for _ in range(run_count):
            seriazlized_object, time = self.serializer.serialize(self.container.load())
            serialization_time_sum += time

            _, time = self.serializer.deserialize(seriazlized_object)
            deserialization_time_sum += time
        
        mean_ser_time = serialization_time_sum / run_count
        mean_deser_time = deserialization_time_sum / run_count
        return mean_ser_time, mean_deser_time
            
    def format_experiment_result(self, mean_ser_time, mean_deser_time):
        if self.serializer is None:
            return ""
        result_string = "{}-{}-{}ms-{}ms".format(
            self.serializer.method_name(), 
            sys.getsizeof(self.serializer.serialize(self.container.load())[0]), 
            mean_ser_time * 1e6, 
            mean_deser_time * 1e6)
        return result_string


if __name__ == '__main__':
    method_name, addr, port = get_env_values("METHOD_NAME", "ADDR", "PORT")
    worker = Worker()
    worker.set_serializer(method_name).set_udp_settings(addr, port).loop()
