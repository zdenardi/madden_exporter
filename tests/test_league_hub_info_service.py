import json

from sqlalchemy.orm import Session

from constants import MOCKS_DIR
from data_classes.madden_classes import (
    HubResponseInfo,
    HubResponseValue,
    MaddenLeagueHubInfo,
)
from models import league_hub_info
from services.league_hub_info_service import LeagueHubInfoService


def test_weekly_information_update_summary(
    session: Session, league_info: league_hub_info
):
    expected_summary = (
        "User Games: \n   snallapa: Houston (4-3-0) @ New England (6-1-0) \n"
    )
    with open(MOCKS_DIR / "league_hub_info.json", "r") as f:
        value = json.load(f)
    response_info = HubResponseInfo(
        tdfid=1, tdfclass="Blaze::Mock", value=HubResponseValue.model_validate(value)
    )
    madden_league_info = MaddenLeagueHubInfo(responseInfo=response_info)
    week_info = LeagueHubInfoService.get_week_info(session, madden_league_info, 1)
    assert week_info.advanced
    assert week_info.old_week == 1
    assert week_info.current_week == 9
    assert week_info.did_summaries_update
    assert week_info.summaries == expected_summary


def test_weekly_information_no_summary_update(
    session: Session, league_info: league_hub_info
):
    ID = 2
    with open(MOCKS_DIR / "league_hub_info.json", "r") as f:
        value = json.load(f)
    response_info = HubResponseInfo(
        tdfid=1, tdfclass="Blaze::Mock", value=HubResponseValue.model_validate(value)
    )
    madden_league_info = MaddenLeagueHubInfo(responseInfo=response_info)
    example_info = league_hub_info.LeagueHubInfo(
        league_id=ID,
        week=9,
        calendar_year=2026,
        summaries="User Games: \n   snallapa: Houston (4-3-0) @ New England (6-1-0) \n",
    )
    session.add(example_info)
    session.flush()
    week_info = LeagueHubInfoService.get_week_info(session, madden_league_info, ID)
    assert week_info.did_summaries_update == False
