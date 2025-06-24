from app.models.models import FixtureClubParticipation, FixturePlayerStatistic, Player, Squad, SquadPlayer, StatisticType
from app.sync.mapper.ObjectMapper import ObjectMapper
from sqlalchemy.orm.session import Session

class FixturePlayerStatisticMapper(ObjectMapper):
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def map_to_object(self, raw_data) -> object:        
        fixture_player_statistic = FixturePlayerStatistic()
        fixture_player_statistic.fixture_club_participation = raw_data["fixture_club_participation"]
        fixture_player_statistic.statistic_type = self.get_statistic_type(raw_data["statistic_type"])
        fixture_player_statistic.value = float(raw_data["value"])
        fixture_player_statistic.squad_player = self.get_squad_player(raw_data["player"], raw_data["fixture_club_participation"])
        
        return fixture_player_statistic

    
    def get_squad_player(self, player, fixture_club_participation: FixtureClubParticipation) -> SquadPlayer:
        return self.session.query(SquadPlayer).join(Player).join(Squad).filter(
            Player.sync_id==player.id,
            Squad.club==fixture_club_participation.club_participation.club,
            Squad.season==fixture_club_participation.club_participation.competition_season.season,
        ).one()
    
    def get_statistic_type(self, statistic_type: str) -> StatisticType:
        return self.session.query(StatisticType).filter(
            StatisticType.statistic_type==statistic_type
        ).one()