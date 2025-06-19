from app.models.models import ClubParticipation, CompetitionSeason, FixtureClubParticipation
from app.sync.source.api_sports_source import ApiSportsSource
from sqlalchemy.orm.session import Session
from apisports_football.Models.Fixtures.Players import Players, Statistics

class FixturePlayerStatisticSource(ApiSportsSource):
    def __init__(self, api, session: Session) -> None:
        super().__init__(api)
        self.session: Session = session
    
    async def fetch(self):# -> Any:
        qry = self.session.query(FixtureClubParticipation).join(FixtureClubParticipation.club_participation)
        fixture_club_participations: list[FixtureClubParticipation] = qry.filter(
            ClubParticipation.is_sync_enabled==True
        )
        
        statistics = []
        for fixture_club_participation in fixture_club_participations:
            data: Players = await self.api.fixtures().players(
                fixture=fixture_club_participation.fixture.sync_id,
                team=fixture_club_participation.club_participation.club.sync_id
            )
            
            statistics += self.hydrate_players_response(data.response, fixture_club_participation)
        
        return statistics
    
    def hydrate_players_response(self, response, fixture_club_participation: FixtureClubParticipation):# -> list:
        statistics = []
        for team in response:
            statistics += self.hydrate_players(team.players, fixture_club_participation)
        
        return statistics
    
    def hydrate_players(self, players: Players, fixture_club_participation: FixtureClubParticipation):# -> list:
        statistics = []
        for player in players:
            statistics_data: Statistics = player.statistics[0]
            
            if (statistics_data.games.minutes is None):
                continue
            
            statistics += self.hydrate_statistics(statistics_data, player.player, fixture_club_participation)
        
        return statistics
    
    def hydrate_statistics(self, statistics: Statistics, player, fixture_club_participation):# -> list:
        stats = []
        
        data = {
            "games.minutes": statistics.games.minutes,
            "games.rating": statistics.games.rating,
            "offsides": statistics.offsides,
            "shots.total": statistics.shots.total,
            "shots.on": statistics.shots.on,
            "goals.total": statistics.goals.total,
            "goals.conceded": statistics.goals.conceded,
            "goals.assists": statistics.goals.assists,
            "goals.saves": statistics.goals.saves,
            "passes.total": statistics.passes.total,
            "passes.key": statistics.passes.key,
            "passes.accuracy": statistics.passes.accuracy,
            "tackles.total": statistics.tackles.total,
            "tackles.blocks": statistics.tackles.blocks,
            "tackles.interceptions": statistics.tackles.interceptions,
            "duels.total": statistics.duels.total,
            "duels.won": statistics.duels.won,
            "dribbles.attempts": statistics.dribbles.attempts,
            "dribbles.success": statistics.dribbles.success,
            "dribbles.past": statistics.dribbles.past,
            "fouls.drawn": statistics.fouls.drawn,
            "fouls.committed": statistics.fouls.committed,
            "cards.yellow": statistics.cards.yellow,
            "cards.red": statistics.cards.red,
            "penalty.won": statistics.penalty.won,
            "penalty.commited": statistics.penalty.commited ,
            "penalty.scored": statistics.penalty.scored,
            "penalty.missed": statistics.penalty.missed,
            "penalty.saved": statistics.penalty.saved
        }
        
        for key, value in data.items():
            if value is None:
                value = 0
            
            stats.append(
                self.generate_dict(player, fixture_club_participation, key, value)
            )
        
        return stats
    
    def generate_dict(self, player, fixture_club_participation, statistic_type, value):# -> dict[str, Any]:
        return {
            "player": player,
            "fixture_club_participation": fixture_club_participation,
            "statistic_type": statistic_type,
            "value": value
        }