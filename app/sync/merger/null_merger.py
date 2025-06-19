from app.sync.merger.merger import Merger

class NullMerger(Merger):
    def merge(self, existing_obj: object, new_obj: object) -> object:
        return existing_obj