from app.models.models import Squad
from app.sync.source.api_sports_source import ApiSportsSource
from apisports_football import Wrapper
from sqlalchemy.orm.session import Session

class SquadPlayerSource(ApiSportsSource):
    def __init__(self, api, session: Session) -> None:
        super().__init__(api)
        self.session: Session = session
    
    async def fetch(self):# -> list:# -> Any:
        qry = self.session.query(Squad)
        squads: list[Squad] = qry.all()
        
        squad_players = []
        for squad in squads:
            for player in await self.fetch_players(squad.club.sync_id, squad.season.sync_id):
                squad_players.append({
                    "player": player.player,
                    "squad": squad,
                })
        
        return squad_players
    
    async def fetch_players(self, team, season):        
        players = []
        
        current = 1
        total = 1
        while(total >= current):
            data = await self.paginated_fetch(team, season, current)
            
            total = data.paging.total
            current += 1
            
            players = players + data.response
                    
        return players
    
    async def paginated_fetch(self, team, season, page):
        return await self.api.players().get(team=team, season=season, page=page)