from avro import schema


datastruct_avro_scheme =  schema.parse("""{
 "namespace": "example.avro",
 "type": "record",
 "name": "DataStruct",
 "fields": [
     {"name": "fbool", "type": "boolean"},
     {"name": "fint",  "type": "int"},
     {"name": "ffloat", "type": "float"}
     {"name": "fstring", "type": "string"}
     {"name": "farray", "type": {"type": "array", "items": "int"}}
     {"name": "fdict", "type": {"type": "map", "values" : "int"}}
 ]
}
""")
