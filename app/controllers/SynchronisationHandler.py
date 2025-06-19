import os
from app.sync.synchronizer import Synchronizer
from apisports_football import Wrapper
from app.sync.synchronizer_registry import SynchronizerRegistry
from app.sync.locator.club_locator import ClubLocator
from app.sync.locator.club_participation_locator import ClubParticipationLocator
from app.sync.locator.competition_locator import CompetitionLocator
from app.sync.locator.competition_season_locator import CompetitionSeasonLocator
from app.sync.locator.fixture_club_participation_locator import FixtureClubParticipationLocator
from app.sync.locator.fixture_locator import FixtureLocator
from app.sync.locator.fixture_player_statistic_locator import FixturePlayerStatisticLocator
from app.sync.locator.player_locator import PlayerLocator
from app.sync.locator.season_locator import SeasonLocator
from app.sync.locator.squad_locator import SquadLocator
from app.sync.locator.squad_player_locator import SquadPlayerLocator
from app.sync.mapper.club_mapper import ClubMapper
from app.sync.mapper.club_participation_mapper import ClubParticipationMapper
from app.sync.mapper.competition_mapper import CompetitionMapper
from app.sync.mapper.competition_season_mapper import CompetitionSeasonMapper
from app.sync.mapper.fixture_club_participation_mapper import FixtureClubParticipationMapper
from app.sync.mapper.fixture_mapper import FixtureMapper
from app.sync.mapper.fixture_player_statistic_mapper import FixturePlayerStatisticMapper
from app.sync.mapper.player_mapper import PlayerMapper
from app.sync.mapper.season_mapper import seasonMapper
from app.sync.mapper.squad_mapper import squadMapper
from app.sync.mapper.squad_player_mapper import SquadPlayerMapper
from app.sync.merger.null_merger import NullMerger
from app.sync.merger.club_merger import ClubMerger
from app.sync.merger.competition_merger import CompetitionMerger
from app.sync.merger.player_merger import PlayerMerger
from app.sync.source.competition_source import CompetitionSource
from app.sync.source.club_source import ClubSource
from app.sync.source.competition_season_source import CompetitionSeasonSource
from app.sync.source.fixture_club_participation import FixtureClubParticipationSource
from app.sync.source.fixture_player_statistic_source import FixturePlayerStatisticSource
from app.sync.source.fixture_source import FixtureSource
from app.sync.source.season_source import SeasonSource
from app.sync.source.squad_player_source import SquadPlayerSource
from app.sync.source.squad_source import SquadSource
from app.sync.storage.database_storage import databaseStorage
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class SynchronizationHandler():
    def __init__(self) -> None:
        self.api = Wrapper(os.getenv("API_FOOTBALL_API_KEY"))
        self.engine = create_engine(os.getenv("DATABASE_CONNECTION"))
    
    def run(self) -> None:
        self.synchronise()
    
    def synchronise(self) -> None:
        registry = SynchronizerRegistry()
        
        session = self.create_session()
        database_storage = databaseStorage(session)
        
        registry.register(
            Synchronizer(
                "competition",
                CompetitionSource(self.api),
                CompetitionMapper(),
                CompetitionLocator(session),
                database_storage,
                CompetitionMerger()
            )
        )
        
        registry.register(
            Synchronizer(
                "season",
                SeasonSource(self.api),
                seasonMapper(),
                SeasonLocator(session),
                database_storage,
                NullMerger()
            )
        )
        
        registry.register(
            Synchronizer(
                "competition_season",
                CompetitionSeasonSource(self.api),
                CompetitionSeasonMapper(session),
                CompetitionSeasonLocator(session),
                database_storage,
                NullMerger()
            )
        )
        
        registry.register(
            Synchronizer(
                "club",
                ClubSource(self.api, session),
                ClubMapper(),
                ClubLocator(session),
                database_storage,
                ClubMerger()
            )
        )
        
        registry.register(
            Synchronizer(
                "club_participation",
                ClubSource(self.api, session),
                ClubParticipationMapper(session),
                ClubParticipationLocator(session),
                database_storage,
                NullMerger()
            )
        )
        
        registry.register(
            Synchronizer(
                "squad",
                SquadSource(session),
                squadMapper(),
                SquadLocator(session),
                database_storage,
                NullMerger()
            )
        )
        
        registry.register(
            Synchronizer(
                "player",
                SquadPlayerSource(self.api, session),
                PlayerMapper(),
                PlayerLocator(session),
                database_storage,
                PlayerMerger()
            )
        )
        
        registry.register(
            Synchronizer(
                "squad_player",
                SquadPlayerSource(self.api, session),
                SquadPlayerMapper(session),
                SquadPlayerLocator(session),
                database_storage,
                NullMerger()
            )
        )
        
        fixture_source = FixtureSource(self.api, session)
        registry.register(
            Synchronizer(
                "fixture",
                fixture_source,
                FixtureMapper(),
                FixtureLocator(session),
                database_storage,
                NullMerger()
            )
        )
        
        registry.register(
            Synchronizer(
                "fixture_club_participation",
                FixtureClubParticipationSource(fixture_source),
                FixtureClubParticipationMapper(session),
                FixtureClubParticipationLocator(session),
                database_storage,
                NullMerger()
            )
        )
        
        registry.register(
            Synchronizer(
                "fixture_player_statistic",
                FixturePlayerStatisticSource(self.api, session),
                FixturePlayerStatisticMapper(session),
                FixturePlayerStatisticLocator(session),
                database_storage,
                NullMerger()
            )
        )
        
        registry.run_all()
        
        session.close()
    
    def create_session(self) -> Session:
        Session = sessionmaker(bind=self.engine)
        return Session()