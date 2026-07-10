import pytest
from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import (
    DefensiveStat,
    Game,
    KickingStat,
    PassingStat,
    Player,
    PuntingStat,
    ReceivingStat,
    RushingStat,
    TeamInfo,
)
from models.helper_classes import Base

TEST_URL = "postgresql+psycopg://madden:madden@localhost:5432/madden_test"

engine = create_engine(
    TEST_URL,
    echo=True,
)

SessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    yield

    Base.metadata.drop_all(engine)


@pytest.fixture
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def team_2(session: Session):
    team_2 = TeamInfo(
        team_id=2,
        abbr_name="Team 2",
        city_name="City 2",
        display_name="Display Name 2",
        injury_count=0,
        nick_name="Second",
        ovr_rating=50,
        primary_color=2,
        secondary_color=3,
    )
    session.add(team_2)
    session.flush()
    return team_2


@pytest.fixture
def team_1(session: Session):
    team_1 = TeamInfo(
        team_id=1,
        abbr_name="Team 1",
        city_name="City 1",
        display_name="Display Name 1",
        injury_count=0,
        nick_name="First",
        ovr_rating=99,
        primary_color=1,
        secondary_color=2,
    )
    session.add(team_1)
    session.flush()
    return team_1


@pytest.fixture
def game(session: Session, team_1, team_2):
    game = Game(
        away_score=21,
        home_score=24,
        schedule_id=1,
        season_index=1,
        status=3,
        week_index=3,
        away_team_id=team_1.team_id,
        home_team_id=team_2.team_id,
    )
    session.add(game)
    session.flush()
    return game


@pytest.fixture
def player(session: Session, team_1: TeamInfo):
    player = Player(
        roster_id=1,
        age=20,
        college="Baldwin Wallace College",
        first_name="John",
        last_name="Doe",
        position="QB",
        is_active=True,
        jersey_num=5,
        years_pro=3,
        ratings={},
        team=team_1,
        team_id=team_1.team_id,
    )
    session.add(player)
    session.flush()
    return player


@pytest.fixture
def passing_stat(session: Session, game: Game, team_1: TeamInfo, player: Player):
    passing_stat = PassingStat(
        pass_att=38,
        pass_comp=24,
        pass_comp_pct=63.1579,
        pass_ints=0,
        pass_longest=36,
        pass_pts=0,
        passer_rating=100.3,
        pass_sacks=1,
        pass_tds=2,
        pass_yds=256,
        pass_yds_per_att=6.73684,
        pass_yds_per_game=253.529,
        roster_id=player.roster_id,
        team_id=team_1.team_id,
        season=1,
        week=1,
        stage=1,
        game=game,
    )
    session.add(passing_stat)
    session.flush()
    return passing_stat


@pytest.fixture
def rushing_stat(session: Session, game: Game, team_1: TeamInfo, player: Player):
    rushing_stat = RushingStat(
        rush_att=7,
        rush_broken_tackles=1,
        rush_fum=0,
        rush_tds=1,
        rush_to_pct=0.0,
        rush_20_plus_yards=0,
        rush_yds_after_contact=1,
        rush_yds=23,
        rush_longest=5,
        rush_yds_per_att=3.28571,
        rush_yds_per_game=19.4,
        roster_id=player.roster_id,
        team_id=team_1.team_id,
        season=1,
        week=1,
        stage=1,
        game=game,
    )
    session.add(rushing_stat)
    session.flush()
    return rushing_stat


@pytest.fixture
def def_stat(session: Session, game: Game, team_1: TeamInfo, player: Player):
    def_stat = DefensiveStat(
        game=game,
        game_id=game.id,
        roster_id=player.roster_id,
        season=game.season_index,
        stage=0,
        team_id=game.home_team_id,
        week=game.week_index,
        def_catch_allowed=0,
        def_deflections=1,
        def_forced_fum=0,
        def_fum_rec=1,
        def_ints=1,
        def_int_return_yds=27,
        def_pts=0,
        def_sacks=1,
        def_safeties=0,
        def_tds=0,
        def_total_tackles=5,
    )
    session.add(def_stat)
    session.flush()
    return def_stat


@pytest.fixture
def punting_stat(session: Session, game: Game, team_1: TeamInfo, player: Player):
    punt_stat = PuntingStat(
        game=game,
        game_id=game.id,
        roster_id=player.roster_id,
        season=game.season_index,
        stage=0,
        team_id=game.home_team_id,
        week=game.week_index,
        punt_blocked=0,
        punt_yds=43,
        punts_in_20=1,
        punt_longest=40,
        punt_tbs=1,
        punt_net_yds_per_att=25.0,
        punt_net_yds=25,
        punt_att=1,
        punt_yds_per_att=43.0,
    )
    session.add(punt_stat)
    session.flush()
    return punt_stat


@pytest.fixture
def kicking_stat(session: Session, game: Game, team_1: TeamInfo, player: Player):
    kicking_stat = KickingStat(
        game=game,
        game_id=game.id,
        roster_id=player.roster_id,
        season=game.season_index,
        stage=0,
        team_id=game.home_team_id,
        week=game.week_index,
        kick_pts=0,
        fg_att=2,
        fg_50_plus_att=0,
        fg_50_plus_made=0,
        fg_longest=52,
        fg_made=2,
        fg_comp_pct=100.0,
        kick_off_att=3,
        kick_off_tbs=0,
        xp_att=3,
        xp_made=2,
        xp_comp_pct=66.6667,
    )
    session.add(kicking_stat)
    session.flush()
    return kicking_stat


@pytest.fixture
def rec_stat(session: Session, game: Game, team_1: TeamInfo, player: Player):
    stat = ReceivingStat(
        rec_catches=3,
        rec_catch_pct=100.0,
        rec_drops=0,
        rec_longest=20,
        rec_pts=0,
        rec_tds=0,
        rec_to_pct=0.0,
        rec_yds_after_catch=18,
        rec_yac_per_catch=6.0,
        rec_yds=29,
        rec_yds_per_catch=9.66667,
        rec_yds_per_game=36.0,
        roster_id=player.roster_id,
        team_id=team_1.team_id,
        season=1,
        week=1,
        stage=1,
        game=game,
    )
    session.add(stat)
    session.flush()
    return stat
