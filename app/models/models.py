from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class StatisticType(Base):
    __tablename__ = "statistic_type"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    statistic_type = Column(String(255), nullable=False)
    is_included_in_analysis = Column(Boolean, nullable=False)

    statistics = relationship("FixturePlayerStatistic", back_populates="statistic_type")


class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    birth = Column(Date, nullable=False)
    photo_url = Column(String(255), nullable=False)
    sync_id = Column(Integer, nullable=False)

    squad_players = relationship("SquadPlayer", back_populates="player")


class Squad(Base):
    __tablename__ = "squad"
    id = Column(Integer, primary_key=True)
    club_id = Column(Integer, ForeignKey("club.id"), nullable=False)
    season_id = Column(Integer, ForeignKey("season.id"), nullable=False)

    club = relationship("Club", back_populates="squads")
    season = relationship("Season", back_populates="squads")
    players = relationship("SquadPlayer", back_populates="squad")


class SquadPlayer(Base):
    __tablename__ = "squad_player"
    id = Column(Integer, primary_key=True)
    squad_id = Column(Integer, ForeignKey("squad.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    type = Column(String(255), nullable=True)
    role_group = Column(String(255), nullable=True)

    squad = relationship("Squad", back_populates="players")
    player = relationship("Player", back_populates="squad_players")
    stats = relationship("FixturePlayerStatistic", back_populates="squad_player")


class Club(Base):
    __tablename__ = "club"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    sync_id = Column(Integer, nullable=False)

    squads = relationship("Squad", back_populates="club")
    participations = relationship("ClubParticipation", back_populates="club")


class Season(Base):
    __tablename__ = "season"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    sync_id = Column(Integer, nullable=False)
    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)

    squads = relationship("Squad", back_populates="season")
    competition_seasons = relationship("CompetitionSeason", back_populates="season")


class Competition(Base):
    __tablename__ = "competition"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    sync_id = Column(Integer, nullable=False)

    competition_seasons = relationship("CompetitionSeason", back_populates="competition")


class CompetitionSeason(Base):
    __tablename__ = "competition_season"
    id = Column(Integer, primary_key=True)
    competition_id = Column(Integer, ForeignKey("competition.id"), nullable=False)
    season_id = Column(Integer, ForeignKey("season.id"), nullable=False)
    is_sync_enabled = Column(Boolean, nullable=False)

    competition = relationship("Competition", back_populates="competition_seasons")
    season = relationship("Season", back_populates="competition_seasons")
    participations = relationship("ClubParticipation", back_populates="competition_season")
    fixtures = relationship("Fixture", back_populates="competition_season")


class ClubParticipation(Base):
    __tablename__ = "club_participation"
    id = Column(Integer, primary_key=True)
    club_id = Column(Integer, ForeignKey("club.id"), nullable=False)
    competition_season_id = Column(Integer, ForeignKey("competition_season.id"), nullable=False)
    is_sync_enabled = Column(Boolean, nullable=False)

    club = relationship("Club", back_populates="participations")
    competition_season = relationship("CompetitionSeason", back_populates="participations")
    fixture_links = relationship("FixtureClubParticipation", back_populates="club_participation")


class Fixture(Base):
    __tablename__ = "fixture"
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    competition_season_id = Column(Integer, ForeignKey("competition_season.id"), nullable=False)
    sync_id = Column(Integer, nullable=False)

    competition_season = relationship("CompetitionSeason", back_populates="fixtures")
    clubs = relationship("FixtureClubParticipation", back_populates="fixture")


class FixtureClubParticipation(Base):
    __tablename__ = "fixture_club_participation"
    id = Column(Integer, primary_key=True)
    fixture_id = Column(Integer, ForeignKey("fixture.id"), nullable=False)
    club_participation_id = Column(Integer, ForeignKey("club_participation.id"), nullable=False)
    role = Column(String(255), nullable=False)

    fixture = relationship("Fixture", back_populates="clubs")
    club_participation = relationship("ClubParticipation", back_populates="fixture_links")
    player_statistics = relationship("FixturePlayerStatistic", back_populates="fixture_club_participation")


class FixturePlayerStatistic(Base):
    __tablename__ = "fixture_player_statistic"
    id = Column(Integer, primary_key=True)
    fixture_club_participation_id = Column(Integer, ForeignKey("fixture_club_participation.id"), nullable=False)
    squad_player_id = Column(Integer, ForeignKey("squad_player.id"), nullable=False)
    statistic_type_id = Column(Integer, ForeignKey("statistic_type.id"), nullable=False)
    value = Column(Float, nullable=False)

    fixture_club_participation = relationship("FixtureClubParticipation", back_populates="player_statistics")
    squad_player = relationship("SquadPlayer", back_populates="stats")
    statistic_type = relationship("StatisticType", back_populates="statistics")

class SquadPlayerComparison(Base):
    __tablename__ = "squad_player_comparison"
    id = Column(Integer, primary_key=True)
    squad_player_1_id = Column(Integer, ForeignKey("squad_player.id"), nullable=False)
    squad_player_2_id = Column(Integer, ForeignKey("squad_player.id"), nullable=False)
    
    squad_player_1 = relationship("SquadPlayer", foreign_keys=[squad_player_1_id])
    squad_player_2 = relationship("SquadPlayer", foreign_keys=[squad_player_2_id])