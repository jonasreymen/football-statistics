from typing import List
from apisports_football.Models.Leagues.Leagues import Leagues, Response
from apisports_football import Wrapper
from app.sync.source.api_sports_source import ApiSportsSource

class CompetitionSeasonSource(ApiSportsSource):    
    async def fetch(self) -> List[Response]:
        data: Leagues = await self.api.leagues().get(id=144)
        leagues = data.response
        
        competition_seasons = []
        for league in leagues:
            for season in league.seasons:
                competition_seasons.append({"season": season, "competition": league.league})
        
        return competition_seasons