from abc import ABCMeta, abstractmethod

class BaseProtocol(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def download(self, url, target, chunk_size):
        pass
