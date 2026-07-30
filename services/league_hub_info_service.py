from sqlalchemy import select
from sqlalchemy.orm import Session

from data_classes.data_classes import WeekInformation
from data_classes.madden_classes import MaddenLeagueHubInfo
from models.LeagueHubInfo import LeagueHubInfo


class LeagueHubInfoService:
    @staticmethod
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

    @staticmethod
    def get_week_info(
        session: Session, hub_info: MaddenLeagueHubInfo, league_id: int
    ) -> WeekInformation:
        league = session.scalar(
            select(LeagueHubInfo).where(LeagueHubInfo.league_id == league_id)
        )

        new_week = hub_info.responseInfo.value.get_week()
        new_year = hub_info.responseInfo.value.get_year()
        summaries = hub_info.responseInfo.value.get_human_game_summaries()
        summary_text = "User Games: \n"
        for summary in summaries:
            summary_text += f"   {summary['user_name']}: {summary['summary']} \n"

        if league is None:
            LeagueHubInfoService.upsert_league_info(session, hub_info, league_id)
            return WeekInformation(
                advanced=True,
                old_week=None,
                current_week=new_week,
                old_year=None,
                current_year=new_year,
                did_summaries_update=True,
                summaries=summary_text,
            )

        old_week = league.week
        old_year = league.calendar_year

        advanced = old_week != new_week or old_year != new_year
        if advanced:
            league.week = new_week
            league.calendar_year = new_year
            league.summaries = summary_text

        are_new_summaries = summary_text != league.summaries

        if are_new_summaries:
            league.summaries = summary_text

        return WeekInformation(
            advanced=advanced,
            old_week=old_week,
            current_week=new_week,
            old_year=old_year,
            current_year=new_year,
            did_summaries_update=are_new_summaries,
            summaries=summary_text,
        )
