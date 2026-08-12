from sqlalchemy.orm import Session

from data_classes.madden_classes import MaddenTeamStat
from models.ea_token import EATokenInfo
from services.ea_auth_service import get_blaze_session, get_EA_token_info
from services.madden_data_service import (
    get_defensive_stats,
    get_free_agents,
    get_kicking_stats,
    get_madden_league_hub,
    get_madden_league_info,
    get_passing_stats,
    get_punting_stats,
    get_receiving_stats,
    get_rushing_stats,
    get_standings,
    get_team_roster,
    get_team_stats,
    get_teams,
    get_weekly_schedule,
)

# These tests call the actual EA apis.


def test_get_leagues(session: Session, EAToken: EATokenInfo):
    b_session = get_blaze_session(EAToken)
    league_info = get_madden_league_info(EAToken, b_session)
    assert league_info is not None


def test_get_league_hub(session: Session, EAToken: EATokenInfo):
    b_session = get_blaze_session(EAToken)
    league_info = get_madden_league_hub(EAToken, b_session)
    assert league_info["success"] is True


def test_get_teams(session):
    token = get_EA_token_info(session)
    b_session = get_blaze_session(token)

    teams = get_teams(token, b_session, 27435432)
    assert teams is not None
    assert len(teams) == 32


def test_get_standings(session):
    token = get_EA_token_info(session)
    b_session = get_blaze_session(token)

    standings = get_standings(token, b_session, 27435432)
    assert standings is not None
    assert len(standings) == 32


def test_get_weekly_schedule(session):
    token = get_EA_token_info(session)
    b_session = get_blaze_session(token)

    schedule = get_weekly_schedule(token, b_session, 27435432)
    assert schedule is not None


def test_get_rushing_stats(session):
    token = get_EA_token_info(session)
    b_session = get_blaze_session(token)

    stats = get_rushing_stats(token, b_session, 27435432, 1, 1)
    assert stats is not None


def test_get_passing_stats(session):
    token = get_EA_token_info(session)
    b_session = get_blaze_session(token)

    stats = get_passing_stats(token, b_session, 27435432, 1, 1)
    assert stats is not None


def test_get_punting_stats(session):
    token = get_EA_token_info(session)
    b_session = get_blaze_session(token)

    stats = get_punting_stats(token, b_session, 27435432, 1, 1)
    assert stats is not None


def test_get_receiving_stats(session):
    token = get_EA_token_info(session)
    b_session = get_blaze_session(token)

    stats = get_receiving_stats(token, b_session, 27435432, 1, 1)
    assert stats is not None


def test_get_defensive_stats(session):
    token = get_EA_token_info(session)
    b_session = get_blaze_session(token)

    stats = get_defensive_stats(token, b_session, 27435432, 1, 1)
    assert stats is not None


def test_get_kicking_stats(session):
    token = get_EA_token_info(session)
    b_session = get_blaze_session(token)

    stats = get_kicking_stats(token, b_session, 27435432, 1, 1)
    assert stats is not None


def test_get_team_roster(session):
    token = get_EA_token_info(session)
    b_session = get_blaze_session(token)

    players = get_team_roster(token, b_session, 27435432, 1)
    assert players is not None


def test_get_free_agents(session):
    token = get_EA_token_info(session)
    b_session = get_blaze_session(token)

    agents = get_free_agents(token, b_session, 27435432)
    assert agents is not None


def test_get_team_stats(session):
    token = get_EA_token_info(session)
    b_session = get_blaze_session(token)

    stats: list[MaddenTeamStat] = get_team_stats(token, b_session, 27435432, 0, 1)
    assert stats is not None
    assert len(stats) == 32
