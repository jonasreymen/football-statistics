from app.models.models import Competition, Season
from app.sync.locator.locator import Locator
from typing import Optional
from sqlalchemy.orm.session import Session
import sqlalchemy.orm.exc as exc

class SeasonLocator(Locator):
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def locate(self, obj: Season) -> Optional[object]:
        qry = self.session.query(Season)
        
        try:
            return qry.filter(Season.sync_id==obj.sync_id).one()
        except exc.NoResultFound as e:
            return