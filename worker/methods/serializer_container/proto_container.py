from methods.serializer_container.base_container import BaseSerializerContainer


class ProtoSerializerContainer(BaseSerializerContainer):
    def __init__(self, store_object=None, cls=None, ser_kwargs: dict = ..., deser_kwargs: dict = ...) -> None:
        super().__init__(store_object, ser_kwargs, deser_kwargs)
        self.cls = cls

    def store(self, store_object):
        self.store_object = store_object

    def load(self):
        return self.store_object
