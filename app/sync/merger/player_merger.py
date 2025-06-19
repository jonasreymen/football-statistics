from app.models.models import Player
from app.sync.merger.merger import Merger

class PlayerMerger(Merger):
    def merge(self, existing_obj: Player, new_obj: Player) -> object:
        existing_obj.name = new_obj.name
        existing_obj.firstname = new_obj.firstname
        existing_obj.lastname = new_obj.lastname
        existing_obj.birth = new_obj.birth
        existing_obj.photo_url = new_obj.photo_url
        
        return existing_obj