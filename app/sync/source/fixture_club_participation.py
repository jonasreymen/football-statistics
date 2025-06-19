from typing import List
from app.sync.role import Role
from apisports_football.Models.Fixtures.Fixtures import FixtureInfo

from app.sync.source.fixture_source import FixtureSource
from app.sync.source.source import Source

class FixtureClubParticipationSource(Source):
    def __init__(self, fixture_source: FixtureSource) -> None:
        self.fixture_source: FixtureSource = fixture_source
    
    def fetch_data(self) -> List:
        fixtures: List = self.fixture_source.fetch_data()
        
        data = []
        for fixture_data in fixtures:
            fixture_info: FixtureInfo = fixture_data["fixture_info"]

            data.append(
                self.generate_dict(
                    fixture_info,
                    fixture_info.teams.home,
                    Role.HOME.value
                )
            )
            data.append(
                self.generate_dict(
                    fixture_info,
                    fixture_info.teams.away,
                    Role.AWAY.value
                )
            )
        
        return data

    
    def generate_dict(self, fixture_info, team, role: str):
        return {
            "fixture_info": fixture_info,
            "role": role,
            "club": team
        }