from app.models.models import Player
from app.sync.locator.locator import Locator
from typing import Optional
from sqlalchemy.orm.session import Session
import sqlalchemy.orm.exc as exc

class PlayerLocator(Locator):
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def locate(self, obj: Player) -> Optional[object]:
        qry = self.session.query(Player)
        
        try:
            return qry.filter(Player.sync_id==obj.sync_id).one()
        except exc.NoResultFound as e:
            return