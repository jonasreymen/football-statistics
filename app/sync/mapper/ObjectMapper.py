from abc import ABC, abstractmethod

class ObjectMapper(ABC):
    @abstractmethod
    def map_to_object(self, raw_data) -> object:
        raise NotImplementedError()