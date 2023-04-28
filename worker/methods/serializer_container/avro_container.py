from base_container import BaseSerializerContainer


class AvroSerializerContainer(BaseSerializerContainer):
    def __init__(self, store_object=None, schema=None, ser_kwargs: dict = ..., deser_kwargs: dict = ...) -> None:
        super().__init__(store_object, ser_kwargs, deser_kwargs)
        self.schema = schema

    def get_schema(self):
        return self.schema

    def store(self, store_object):
        self.store_object = store_object

    def load(self):
        return self.store_object
