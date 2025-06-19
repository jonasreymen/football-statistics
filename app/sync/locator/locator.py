from abc import ABC, abstractmethod
from typing import Optional

class Locator(ABC):
    @abstractmethod
    def locate(self, obj: object) -> Optional[object]:
        pass