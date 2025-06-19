from app.models.models import Player
from app.sync.mapper.ObjectMapper import ObjectMapper

class PlayerMapper(ObjectMapper):
    def map_to_object(self, raw_data) -> object:
        player_data = raw_data["player"]
        
        player = Player()
        player.sync_id = player_data.id
        player.name = player_data.name
        player.firstname = player_data.firstname
        player.lastname = player_data.lastname
        player.birth = player_data.birth.date
        player.photo_url = player_data.photo
        
        return player