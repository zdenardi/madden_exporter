from datetime import datetime, timedelta, timezone

from requests import Session

from data_classes.madden_classes import MaddenTeamStat
from models.ea_token import EATokenInfo
from services.ea_services import (
    get_auth_code,
    get_blaze_session,
    get_defensive_stats,
    get_EA_access_token,
    get_EA_jws_token,
    get_EA_token_info,
    get_free_agents,
    get_kicking_stats,
    get_madden_league_hub,
    get_madden_league_info,
    get_passing_stats,
    get_persona_auth_code,
    get_personas,
    get_punting_stats,
    get_receiving_stats,
    get_rushing_stats,
    get_standings,
    get_team_roster,
    get_team_stats,
    get_teams,
    get_weekly_schedule,
    refresh_token,
)


# These tests can not really run without connecting to EA. If there is ever a CI/CD ,this would be skipped or mocked
# I used these not so much for internal testing, but to reverse engineer the calls for the Madden API
def test_get_code():
    code = get_auth_code()
    assert code is not None


def test_get_token():
    code = get_auth_code()
    token = get_EA_access_token(code)
    assert token is not None


def test_get_personas():
    code = get_auth_code()
    token = get_EA_access_token(code)
    personas = get_personas(token)
    assert personas is not None


def test_get_persona_auth():
    code = get_auth_code()
    token = get_EA_access_token(code)
    personas = get_personas(token)
    persona = personas[0]
    p_code = get_persona_auth_code(token["access_token"], persona)
    assert p_code is not None


def test_get_EA_jws():
    code = get_auth_code()
    token = get_EA_access_token(code)
    personas = get_personas(token)
    persona = personas[0]
    p_code = get_persona_auth_code(token["access_token"], persona)
    ea_jws = get_EA_jws_token(p_code)
    assert ea_jws is not None


def test_refresh_token():
    code = get_auth_code()
    token = get_EA_access_token(code)
    personas = get_personas(token)
    persona = personas[0]
    p_code = get_persona_auth_code(token["access_token"], persona)
    ea_jws = get_EA_jws_token(p_code)
    new_token = refresh_token(ea_jws["refresh_token"])
    assert new_token is not None
    assert new_token["access_token"] is not None
    assert new_token["expires_in"] is not None
    assert new_token["refresh_token"] is not None


def test_get_blaze_session():
    code = get_auth_code()
    token = get_EA_access_token(code)
    personas = get_personas(token)
    persona = personas[0]
    p_code = get_persona_auth_code(token["access_token"], persona)
    ea_jws_token = get_EA_jws_token(p_code)
    expires_at = datetime.now(timezone.utc) + timedelta(
        seconds=ea_jws_token["expires_in"]
    )
    token_info = EATokenInfo(
        access_token=ea_jws_token["access_token"],
        refresh_token=ea_jws_token["refresh_token"],
        expires_at=expires_at,
    )
    session = get_blaze_session(token_info)
    assert session.request_id is not None
    assert session.blaze_id is not None
    assert session.session_key is not None


def test_get_leagues(session: Session, EAToken: EATokenInfo):
    session = get_blaze_session(EAToken)
    league_info = get_madden_league_info(EAToken, session)
    assert league_info is not None


def test_get_league_hub(session: Session, EAToken: EATokenInfo):
    session = get_blaze_session(EAToken)
    league_info = get_madden_league_hub(EAToken, session)
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
