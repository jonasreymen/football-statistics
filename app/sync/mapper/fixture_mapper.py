from app.models.models import Fixture
from app.sync.mapper.ObjectMapper import ObjectMapper
from apisports_football.Models.Fixtures.Fixtures import Fixture as ApiFixture

class FixtureMapper(ObjectMapper):
    def map_to_object(self, raw_data) -> object:
        fixture_data: ApiFixture = raw_data["fixture"]
        
        fixture = Fixture()
        fixture.sync_id = fixture_data.id
        fixture.competition_season = raw_data["club_participation"].competition_season
        fixture.date = fixture_data.date
        
        return fixture