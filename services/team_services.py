from sqlalchemy.orm import Session

from models import TeamInfo
from models.madden_classes import MaddenTeam


def upsert_team(session: Session, team: MaddenTeam):
    existing = session.get(TeamInfo, team.teamId)

    if existing:
        existing.display_name = team.displayName
        existing.city_name = team.cityName
        existing.abbr_name = team.abbrName
        existing.injury_count = team.injuryCount
        existing.nick_name = team.nickName
        existing.ovr_rating = team.ovrRating
        existing.primary_color = team.primaryColor
        existing.secondary_color = team.secondaryColor
        return existing
    else:
        team_info = TeamInfo(
            team_id=team.teamId,
            display_name=team.displayName,
            city_name=team.cityName,
            abbr_name=team.abbrName,
            injury_count=team.injuryCount,
            nick_name=team.nickName,
            ovr_rating=team.ovrRating,
            primary_color=team.primaryColor,
            secondary_color=team.secondaryColor,
        )
        session.add(team_info)
        return team_info
