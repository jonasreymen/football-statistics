from app.models.models import Player, SquadPlayer
from app.sync.mapper.ObjectMapper import ObjectMapper
from sqlalchemy.orm.session import Session

class SquadPlayerMapper(ObjectMapper):
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def map_to_object(self, raw_data) -> object:        
        squad_player = SquadPlayer()
        squad_player.squad = raw_data["squad"]
        squad_player.player = self.session.query(Player).filter(
            Player.sync_id==raw_data["player"].id
        ).one()
        
        print(raw_data)
        
        return squad_player