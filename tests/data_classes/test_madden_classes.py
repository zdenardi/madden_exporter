import json
from pathlib import Path

from data_classes.madden_classes import HubResponseValue

MOCKS_DIR = Path(__file__).parent.parent.parent / "mocks"


def test_league_hub_info():
    expected_summaries = [{"user_name": "snallapa", "summary": "@ Texans"}]

    with open(MOCKS_DIR / "league_hub_info.json", "r") as f:
        value = json.load(f)
    value = HubResponseValue.model_validate(value)
    summaries = value.get_human_game_summaries()
    week = value.get_week()
    year = value.get_year()
    assert summaries == expected_summaries
    assert week == 9
    assert year == 2026


def test_summaries():
    summaries = [
        {"user_name": "snallapa", "summary": "@ Texans"},
        {"user_name": "fizz", "summary": "@ Buzz"},
    ]
    msg = "Games: "
    for summary in summaries:
        msg += f"{summary['user_name']}: {summary['summary']} \n"
    print(msg)
