from app.sync.storage.storage import Storage
from typing import List

class NullStorage(Storage):
    def update(self, obj: List[object]) -> None:
        return

    def insert(self, obj: List[object]) -> None:
        return