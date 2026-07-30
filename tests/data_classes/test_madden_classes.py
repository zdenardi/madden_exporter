import json
from pathlib import Path

from constants import MOCKS_DIR
from data_classes.madden_classes import HubResponseValue


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
