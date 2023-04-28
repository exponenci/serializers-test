from abc import abstractmethod, ABC


class BaseSerializerContainer(ABC):
    def __init__(self, store_object=None, ser_kwargs: dict = dict(), deser_kwargs: dict = dict()) -> None:
        self.ser_kwargs = ser_kwargs
        self.deser_kwargs = deser_kwargs
        self.store_object = store_object

    def store(self, store_object):
        self.store_object = store_object

    def load(self):
        return self.store_object
