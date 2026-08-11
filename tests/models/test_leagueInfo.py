import json
from pathlib import Path

from models.league_info import LeagueInfo

MOCKS_DIR = Path(__file__).parent.parent.parent / "mocks"


def test_convert_to_league_info():
    with open(MOCKS_DIR / "league_info.json") as f:
        league_info = json.load(f)
    league_info = LeagueInfo.convert_from_madden(league_info)
    assert league_info.week == 10
    assert league_info.calendar_year == 2038
    assert league_info.league_id == 27435432
