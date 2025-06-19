from typing import List
from apisports_football.Models.Fixtures.Fixtures import Fixtures, FixtureInfo
from apisports_football import Wrapper
from app.models.models import ClubParticipation
from app.sync.source.api_sports_source import ApiSportsSource
from sqlalchemy.orm.session import Session

class FixtureSource(ApiSportsSource):
    def __init__(self, api, session: Session) -> None:
        super().__init__(api)
        self.session: Session = session
    
    async def fetch(self) -> List:
        qry = self.session.query(ClubParticipation)
        club_participation: list[ClubParticipation] = qry.filter(ClubParticipation.is_sync_enabled==True)
        
        fixture_data = []
        for participation in club_participation:
            data: Fixtures = await self.api.fixtures().get(
                league=participation.competition_season.competition.sync_id,
                season=participation.competition_season.season.sync_id,
                team=participation.club.sync_id
            )
            
            fixture_data += self.generate_fixture_dict(data.response, participation)
        
        return self.remove_duplicates(fixture_data)
    
    def generate_fixture_dict(self, fixtures: List[FixtureInfo], club_participation: ClubParticipation):# -> list:
        mapped = []
        for fixture in fixtures:
            mapped.append({
                "fixture": fixture.fixture,
                "club_participation": club_participation,
                "fixture_info": fixture
            })
        
        return mapped
    
    def remove_duplicates(self, fixtures: List):# -> list:
        mapped = []
        for fixture in fixtures:
            if (fixture["fixture"].id not in mapped):
                mapped.insert(fixture["fixture"].id, fixture)
        
        return mapped