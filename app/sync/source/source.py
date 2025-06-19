from abc import ABC, abstractmethod
from typing import List

class Source(ABC):
    @abstractmethod
    def fetch_data(self) -> List[dict]:
        raise NotImplementedError()