from app.models.models import Competition
from app.sync.merger.merger import Merger

class CompetitionMerger(Merger):
    def merge(self, existing_obj: Competition, new_obj: Competition) -> object:
        existing_obj.name = new_obj.name
        existing_obj.type = new_obj.type
        
        return existing_obj