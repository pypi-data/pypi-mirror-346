import abc


class Plugin(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def name(cls) -> str:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def is_available(cls) -> bool:
        return True

    @abc.abstractmethod
    def process(self, data: str) -> list[str]:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def example_input(cls) -> str:
        raise NotImplementedError
