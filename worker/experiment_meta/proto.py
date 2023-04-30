from experiment_meta.datastruct_pb2 import DataStruct
from experiment_meta.pydict import datastruct_dict

from google.protobuf.json_format import ParseDict


def fast_load(dict_obj):
    tmp = DataStruct()
    ParseDict(dict_obj, tmp)
    return tmp


datastruct_proto = fast_load(datastruct_dict)
