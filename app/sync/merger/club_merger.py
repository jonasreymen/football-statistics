from app.models.models import Club
from app.sync.merger.merger import Merger

class ClubMerger(Merger):
    def merge(self, existing_obj: Club, new_obj: Club) -> object:
        existing_obj.name = new_obj.name
        
        return existing_obj