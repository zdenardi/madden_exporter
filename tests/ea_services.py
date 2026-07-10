from services.ea_service import get_EA_access_token


def test_get_token():
    token = get_EA_access_token()
    assert token is not None
