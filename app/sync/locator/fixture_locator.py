from app.models.models import Fixture
from app.sync.locator.locator import Locator
from typing import Optional
from sqlalchemy.orm.session import Session
import sqlalchemy.orm.exc as exc

class FixtureLocator(Locator):
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def locate(self, obj: Fixture) -> Optional[object]:
        qry = self.session.query(Fixture)
        
        try:
            return qry.filter(Fixture.sync_id==obj.sync_id).one()
        except exc.NoResultFound as e:
            return