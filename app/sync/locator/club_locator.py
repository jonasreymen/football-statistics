from app.models.models import Club
from app.sync.locator.locator import Locator
from typing import Optional
from sqlalchemy.orm.session import Session
import sqlalchemy.orm.exc as exc

class ClubLocator(Locator):
    def __init__(self, session: Session):
        self.session = session
    
    def locate(self, obj: Club) -> Optional[object]:
        qry = self.session.query(Club)
        
        try:
            return qry.filter(Club.sync_id==obj.sync_id).one()
        except exc.NoResultFound as e:
            return