import os
import sys
import json
import socket
import threading

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
        from experiment_meta.proto import datastruct_proto
        return ProtoSerializerContainer(datastruct_proto, DataStruct)
    else:
        return BaseSerializerContainer(datastruct_dict)


class Worker:
    def __init__(self, sock) -> None:
        self.sock = sock
        self.container: Any = None
        self.serializer: Union[SerializerInterface, None] = None

    def set_serializer(self, method_name: str = 'native'):
        self.container = get_container(method_name)
        self.serializer = get_serializer(method_name, self.container)
        return self

    def loop(self):
        if self.serializer is None:
            return
        while True:
            data, request_addr = self.sock.recvfrom(16 * 1024)
            if data == b'get_result':
                result = self.format_experiment_result(*self.run_experiment())
                self.sock.sendto(
                    json.dumps({'status': 'ok', 'result': result}).encode(), 
                    request_addr)
            else:
                self.sock.sendto(
                    json.dumps({'status': 'error', 'info': 'no such method! ({})'.format(
                        self.serializer.method_name())}).encode(), 
                    request_addr)

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
        result_string = "{0}-{1}-{2:.2f}mus-{3:.2f}mus\n".format(
            self.serializer.method_name(), 
            sys.getsizeof(self.serializer.serialize(self.container.load())[0]), 
            mean_ser_time / 1e3, 
            mean_deser_time / 1e3)
        return result_string


if __name__ == '__main__':
    METHOD, SERVICE_PORT, MCAST_GRP = get_env_values("METHOD", "SERVICE_PORT", "MCAST_GRP")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((METHOD.lower(), int(SERVICE_PORT)))

    grp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    grp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    grp_sock.bind(('', int(os.getenv('MCAST_PORT', 9889))))
    grp_sock.setsockopt(
        socket.IPPROTO_IP, 
        socket.IP_ADD_MEMBERSHIP, 
        socket.inet_aton(MCAST_GRP) + socket.inet_aton('0.0.0.0'))

    func = lambda cur_sock: Worker(cur_sock).set_serializer(METHOD).loop()

    ts = []
    for s in [sock, grp_sock]:
        ts.append(threading.Thread(target=func, args=(s,)))
    for t in ts:
        t.start()
    for t in ts:
        t.join()
