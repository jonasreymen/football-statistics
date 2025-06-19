from app.models.models import CompetitionSeason
from app.sync.source.api_sports_source import ApiSportsSource
from apisports_football import Wrapper
from sqlalchemy.orm.session import Session

class ClubSource(ApiSportsSource):
    def __init__(self, api, session: Session) -> None:
        super().__init__(api)
        self.session: Session = session
    
    async def fetch(self):# -> Any:
        qry = self.session.query(CompetitionSeason)
        competitionsSeasons: list[CompetitionSeason] = qry.filter(CompetitionSeason.is_sync_enabled==True)
        
        clubs = {}
        for competitionSeason in competitionsSeasons:
            data = await self.api.teams().get(league=competitionSeason.competition.sync_id, season=competitionSeason.season.sync_id)
            teams = data.response
            
            for team in teams:
                clubs[team.team.id] = {
                    "team": team.team,
                    "competitionSeason": competitionSeason,
                }
        
        return clubs.values()