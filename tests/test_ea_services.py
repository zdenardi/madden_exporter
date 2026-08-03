from datetime import datetime, timedelta, timezone

from requests import Session

from models.EAtoken import EATokenInfo
from services.ea_services import (
    get_auth_code,
    get_blaze_session,
    get_EA_access_token,
    get_EA_jws_token,
    get_EA_token_info,
    get_madden_league_hub,
    get_madden_league_info,
    get_persona_auth_code,
    get_personas,
    get_standings,
    get_teams,
    refresh_token,
)


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
