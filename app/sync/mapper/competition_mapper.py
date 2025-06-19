from app.models.models import Competition
from app.sync.mapper.ObjectMapper import ObjectMapper
from apisports_football.Models.Leagues.Leagues import Response

class CompetitionMapper(ObjectMapper):
    def map_to_object(self, raw_data: Response) -> object:
        competition = Competition()
        
        competition.name = raw_data.league.name
        competition.type = raw_data.league.type
        competition.sync_id = raw_data.league.id
        
        return competition