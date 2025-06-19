from abc import ABC, abstractmethod

class PageNavigatorInterface(ABC):
    @abstractmethod
    def navigate(self, name: str, request_data: dict = {}) -> None:
        pass