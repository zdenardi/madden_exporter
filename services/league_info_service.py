from sqlalchemy import select
from sqlalchemy.orm import Session

from data_classes.madden_classes import MaddenLeagueInfo
from models.LeagueInfo import LeagueInfo
from data_classes.data_classes import WeekInformation


class LeagueInfoService:
    @staticmethod
    def upsert_league_info(
        session: Session,
        info: MaddenLeagueInfo,
    ) -> LeagueInfo:
        league = session.scalar(
            select(LeagueInfo).where(LeagueInfo.league_id == info["leagueId"])
        )

        if league is None:
            league = LeagueInfo.convert_from_madden(info)
            session.add(league)
        else:
            league.calendar_year = info["calendarYear"]
            league.week = int(info["seasonText"].split()[-1])

        session.commit()
        session.refresh(league)
        return league

    @staticmethod
    def did_week_advance(
        session: Session,
        info: MaddenLeagueInfo,
    ) -> WeekInformation:
        league = session.scalar(
            select(LeagueInfo).where(LeagueInfo.league_id == info["leagueId"])
        )

        new_week = int(info["seasonText"].split()[-1])
        new_year = info["calendarYear"]

        if league is None:
            LeagueInfoService.upsert_league_info(session, info)
            return WeekInformation(
                advanced=True,
                old_week=None,
                current_week=new_week,
                old_year=None,
                current_year=new_year,
            )

        old_week = league.week
        old_year = league.calendar_year

        advanced = old_week != new_week or old_year != new_year

        if advanced:
            league.week = new_week
            league.calendar_year = new_year
            session.commit()

        return WeekInformation(
            advanced=advanced,
            old_week=old_week,
            current_week=new_week,
            old_year=old_year,
            current_year=new_year,
        )
