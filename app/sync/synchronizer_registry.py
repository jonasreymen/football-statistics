from csv import Error
from typing import List
from app.sync.synchronizer import Synchronizer

class SynchronizerRegistry:
    def __init__(self) -> None:
        self._synchronizers: List[Synchronizer] = []

    def register(self, synchronizer: Synchronizer) -> None:
        self._synchronizers.append(synchronizer)

    def run_all(self) -> None:
        print("\n🚀 Running all registered synchronizers...\n")
        for sync in self._synchronizers:
            try:
                sync.sync()
            except Exception as e:
                print(f"❌ Error in synchronizer '{sync.name}': {e}")
                
                raise Error(e)