from app.models.models import Club
from app.sync.mapper.ObjectMapper import ObjectMapper
from apisports_football.Models.Teams.Teams import Response

class ClubMapper(ObjectMapper):
    def map_to_object(self, raw_data: Response) -> object:
        club = Club()
        
        club.name = raw_data["team"].name
        club.sync_id = raw_data["team"].id
        
        return club