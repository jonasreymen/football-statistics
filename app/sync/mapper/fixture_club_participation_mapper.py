from app.models.models import Club, ClubParticipation, Competition, CompetitionSeason, FixtureClubParticipation, Season, Fixture
from app.sync.mapper.ObjectMapper import ObjectMapper
from sqlalchemy.orm.session import Session
from apisports_football.Models.Fixtures.Fixtures import Team, FixtureInfo

class FixtureClubParticipationMapper(ObjectMapper):
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def map_to_object(self, raw_data) -> object:
        fixture_info: FixtureInfo = raw_data["fixture_info"]
        fixture = self.session.query(Fixture).filter(Fixture.sync_id==fixture_info.fixture.id).one()
        
        club_data: Team = raw_data["club"]
        club: Club = self.session.query(Club).filter(Club.sync_id==club_data.id).one()
        
        season: Season = self.session.query(Season).filter(Season.sync_id==fixture_info.league.season).one()
        
        competition: Competition = self.session.query(Competition).filter(Competition.sync_id==fixture_info.league.id).one()
        
        competition_season: CompetitionSeason = self.session.query(CompetitionSeason).filter(
            CompetitionSeason.competition==competition,
            CompetitionSeason.season==season
        ).one()
        
        club_participation = self.session.query(ClubParticipation).filter(
            ClubParticipation.club==club,
            ClubParticipation.competition_season==competition_season
        ).one()
        
        fixture_club_participation = FixtureClubParticipation()
        fixture_club_participation.fixture = fixture
        fixture_club_participation.club_participation = club_participation
        fixture_club_participation.role = raw_data["role"]
        
        return fixture_club_participation