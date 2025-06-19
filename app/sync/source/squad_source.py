from sqlalchemy.orm.session import Session
from typing import List
from app.models.models import ClubParticipation, CompetitionSeason
from app.sync.source.source import Source

class SquadSource(Source):
    def __init__(self, session: Session) -> None:
        self.session: Session = session
    
    def fetch_data(self) -> List[dict]:
        qry = self.session.query(ClubParticipation)
        club_participation: list[ClubParticipation] = qry.filter(ClubParticipation.is_sync_enabled==True)
        
        squads = []
        for participation in club_participation:
            competition_season: CompetitionSeason = participation.competition_season
            
            squads.append({
                "club": participation.club,
                "season": competition_season.season
            })
        
        return squads