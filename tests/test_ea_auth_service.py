from datetime import datetime, timedelta, timezone

from models.ea_token import EATokenInfo
from services.ea_auth_service import (
    get_auth_code,
    get_blaze_session,
    get_EA_access_token,
    get_EA_jws_token,
    get_persona_auth_code,
    get_personas,
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
