from app.models.models import Fixture, FixturePlayerStatistic
from app.sync.locator.locator import Locator
from typing import Optional
from sqlalchemy.orm.session import Session
import sqlalchemy.orm.exc as exc

class FixturePlayerStatisticLocator(Locator):
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def locate(self, obj: FixturePlayerStatistic) -> Optional[object]:
        qry = self.session.query(FixturePlayerStatistic)
        
        try:
            return qry.filter(
                FixturePlayerStatistic.fixture_club_participation==obj.fixture_club_participation,
                FixturePlayerStatistic.squad_player==obj.squad_player,
                FixturePlayerStatistic.statistic_type==obj.statistic_type,
            ).one()
        except exc.NoResultFound as e:
            return