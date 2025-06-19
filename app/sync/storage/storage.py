from abc import ABC, abstractmethod
from typing import List

class Storage(ABC):
    @abstractmethod
    def update(self, obj: List[object]) -> None:
        raise NotImplementedError() 

    @abstractmethod
    def insert(self, obj: List[object]) -> None:
        raise NotImplementedError()