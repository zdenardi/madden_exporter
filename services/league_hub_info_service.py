from sqlalchemy import select
from sqlalchemy.orm import Session

from data_classes.data_classes import WeekInformation
from data_classes.madden_classes import MaddenLeagueHubInfo
from models.league_hub_info import LeagueHubInfo


def upsert_league_info(
    session: Session, hub_info: MaddenLeagueHubInfo, league_id: int
) -> LeagueHubInfo:
    info = hub_info.responseInfo.value
    stmt = select(LeagueHubInfo).where(LeagueHubInfo.league_id == league_id)
    league = session.scalar(stmt)

    if league is None:
        league = LeagueHubInfo.convert_from_madden(league_id, hub_info)
        session.add(league)
    else:
        summaries = info.get_human_game_summaries()
        summary_text = "User Games: \n"
        for summary in summaries:
            summary_text += f"   {summary['user_name']}: {summary['summary']} \n"
        league.calendar_year = info.get_year()
        league.summaries = summary_text
        league.week = info.get_week()

    session.commit()
    session.refresh(league)
    return league


def update_league_and_get_week_info(
    session: Session, hub_info: MaddenLeagueHubInfo, league_id: int
) -> WeekInformation:
    league_info = session.scalar(
        select(LeagueHubInfo).where(LeagueHubInfo.league_id == league_id)
    )

    new_week = hub_info.responseInfo.value.get_week()
    new_year = hub_info.responseInfo.value.get_year()
    summaries = hub_info.responseInfo.value.get_human_game_summaries()
    week_index, stage_index, season_index = (
        hub_info.responseInfo.value.get_internal_week_and_stage()
    )
    summary_text = "User Games: \n"
    for summary in summaries:
        summary_text += f"   {summary['user_name']}: {summary['summary']} \n"

    if league_info is None:
        league_info = upsert_league_info(session, hub_info, league_id)
        return WeekInformation(
            advanced=True,
            old_week=None,
            current_week=new_week,
            old_year=None,
            current_year=new_year,
            did_summaries_update=True,
            summaries=summary_text,
            week_index=week_index,
            stage_index=stage_index,
            season_index=season_index,
        )

    old_week = league_info.week
    old_year = league_info.calendar_year
    current_summaries = league_info.summaries
    are_new_summaries = summary_text != current_summaries

    advanced = old_week != new_week or old_year != new_year
    if advanced:
        league_info.week = new_week
        league_info.calendar_year = new_year
        league_info.summaries = summary_text

    elif are_new_summaries:
        league_info.summaries = summary_text

    return WeekInformation(
        advanced=advanced,
        old_week=old_week,
        current_week=new_week,
        old_year=old_year,
        current_year=new_year,
        did_summaries_update=are_new_summaries,
        summaries=summary_text,
        week_index=week_index,
        stage_index=stage_index,
        season_index=season_index,
    )
