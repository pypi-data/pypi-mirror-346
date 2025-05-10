import abc


class Input(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def name(cls):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def is_available(cls):
        raise NotImplementedError

    @abc.abstractmethod
    def read(self) -> str:
        raise NotImplementedError
