from app.models.models import Club, Season, Squad
from app.sync.mapper.ObjectMapper import ObjectMapper

class squadMapper(ObjectMapper):
    def map_to_object(self, raw_data: dict) -> object:
        season: Season = raw_data["season"]
        club: Club = raw_data["club"]
        
        squad = Squad()
        squad.season = season
        squad.club = club
        return squad