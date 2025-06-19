from abc import abstractmethod
from app.sync.source.source import Source
from typing import List
import asyncio
from apisports_football import Wrapper

class ApiSportsSource(Source):
    def __init__(self, api: Wrapper) -> None:
        self.api: Wrapper = api
        
    
    def fetch_data(self) -> List[dict]:
        return asyncio.run(self.fetch())
    
    @abstractmethod
    async def fetch(self):# -> Any:
        raise NotImplementedError()