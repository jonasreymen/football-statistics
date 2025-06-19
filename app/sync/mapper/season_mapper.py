from app.models.models import Season
from app.sync.mapper.ObjectMapper import ObjectMapper

class seasonMapper(ObjectMapper):
    def map_to_object(self, raw_data: int) -> object:
        season = Season()
        season.sync_id = raw_data
        season.name = raw_data
        season.start = raw_data
        season.end = raw_data + 1
        return season