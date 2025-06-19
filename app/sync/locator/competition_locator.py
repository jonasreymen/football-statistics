from app.models.models import Competition
from app.sync.locator.locator import Locator
from typing import Optional
from sqlalchemy.orm.session import Session
import sqlalchemy.orm.exc as exc

class CompetitionLocator(Locator):
    def __init__(self, session: Session):
        self.session = session
    
    def locate(self, obj: Competition) -> Optional[object]:
        qry = self.session.query(Competition)
        
        try:
            return qry.filter(Competition.sync_id==obj.sync_id).one()
        except exc.NoResultFound as e:
            return