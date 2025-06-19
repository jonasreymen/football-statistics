from app.models.models import Squad
from app.sync.locator.locator import Locator
from typing import Optional
from sqlalchemy.orm.session import Session
import sqlalchemy.orm.exc as exc

class SquadLocator(Locator):
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def locate(self, obj: Squad) -> Optional[object]:
        qry = self.session.query(Squad)
        
        try:
            return qry.filter(Squad.season==obj.season, Squad.club==obj.club).one()
        except exc.NoResultFound as e:
            return