from app.models.models import Club, ClubParticipation
from app.sync.mapper.ObjectMapper import ObjectMapper
from apisports_football.Models.Teams.Teams import Response

class ClubParticipationMapper(ObjectMapper):
    def __init__(self, session) -> None:
        self.session = session
    
    def map_to_object(self, raw_data: Response) -> object:
        club_participation = ClubParticipation()
        
        club_participation.club = self.session.query(Club).filter(Club.sync_id==raw_data["team"].id).one()
        club_participation.competition_season = raw_data["competitionSeason"]
        club_participation.is_sync_enabled = False
        
        return club_participation