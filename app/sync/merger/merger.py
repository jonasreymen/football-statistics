from abc import ABC, abstractmethod

class Merger(ABC):
    @abstractmethod
    def merge(self, existing_obj: object, new_obj: object) -> object:
        raise NotImplementedError()