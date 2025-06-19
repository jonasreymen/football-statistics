from app.models.models import Competition, CompetitionSeason
from app.sync.locator.locator import Locator
from typing import Optional
from sqlalchemy.orm.session import Session
import sqlalchemy.orm.exc as exc

class CompetitionSeasonLocator(Locator):
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def locate(self, obj: CompetitionSeason) -> Optional[object]:
        qry = self.session.query(CompetitionSeason)
        
        try:
            return qry.filter(
                CompetitionSeason.competition==obj.competition,
                CompetitionSeason.season==obj.season
            ).one()
        except exc.NoResultFound as e:
            return