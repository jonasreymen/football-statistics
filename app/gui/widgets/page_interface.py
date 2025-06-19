from abc import ABC

class PageInterface(ABC):
    def load(self, data: dict = {}) -> None:
        pass