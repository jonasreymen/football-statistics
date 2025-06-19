from app.sync.source.api_sports_source import ApiSportsSource
from apisports_football import Wrapper

class SeasonSource(ApiSportsSource):
    async def fetch(self):# -> Any:
        data = await self.api.leagues().seasons()
        
        return data.response