from app.models.models import Fixture, FixtureClubParticipation
from app.sync.locator.locator import Locator
from typing import Optional
from sqlalchemy.orm.session import Session
import sqlalchemy.orm.exc as exc

class FixtureClubParticipationLocator(Locator):
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def locate(self, obj: FixtureClubParticipation) -> Optional[object]:
        qry = self.session.query(FixtureClubParticipation)
        
        try:
            return qry.filter(
                FixtureClubParticipation.fixture==obj.fixture,
                FixtureClubParticipation.club_participation==obj.club_participation
            ).one()
        except exc.NoResultFound as e:
            return