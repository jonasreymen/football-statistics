from app.models.models import Competition, CompetitionSeason, Season
from app.sync.mapper.ObjectMapper import ObjectMapper
from sqlalchemy.orm.session import Session

class CompetitionSeasonMapper(ObjectMapper):
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def map_to_object(self, raw_data: dict) -> object:
        competitionSeason = CompetitionSeason()
        
        competitionSeason.season = self.session.query(Season).filter(Season.sync_id==raw_data["season"].year).one()
        competitionSeason.competition = self.session.query(Competition).filter(Competition.sync_id==raw_data["competition"].id).one()
        competitionSeason.is_sync_enabled = False
        
        return competitionSeason