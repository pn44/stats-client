from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod
    def __init__(self, username, password):
        pass


class APIError(Exception):
    def __init__(self, type, message):
        self.type = type
        self.message = message
        return super().__init__("{}: {}".format(type, message))