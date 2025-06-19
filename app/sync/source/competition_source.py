from typing import List
from apisports_football.Models.Leagues.Leagues import Leagues, Response
from apisports_football import Wrapper
from app.sync.source.api_sports_source import ApiSportsSource

class CompetitionSource(ApiSportsSource):    
    async def fetch(self) -> List[Response]:
        data: Leagues = await self.api.leagues().get(id=144)
        
        return data.response