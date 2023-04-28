from datastruct_pb2 import DataStruct
from pydict import datastruct_dict


datastruct_proto = DataStruct()
for k, v in datastruct_dict.items():
    setattr(datastruct_proto, k, v)
