from app.models.models import Club, ClubParticipation
from app.sync.locator.locator import Locator
from typing import Optional
from sqlalchemy.orm.session import Session
import sqlalchemy.orm.exc as exc

class ClubParticipationLocator(Locator):
    def __init__(self, session: Session):
        self.session = session
    
    def locate(self, obj: ClubParticipation) -> Optional[object]:
        qry = self.session.query(ClubParticipation)
        
        try:
            return qry.filter(
                ClubParticipation.club==obj.club,
                ClubParticipation.competition_season==obj.competition_season
            ).one()
        except exc.NoResultFound as e:
            return