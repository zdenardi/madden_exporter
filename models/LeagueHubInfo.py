from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column

from data_classes.madden_classes import MaddenLeagueHubInfo
from models.helper_classes import Base


class LeagueHubInfo(Base):
    __tablename__ = "league_hub_info"
    league_id: Mapped[int] = mapped_column(primary_key=True)
    week: Mapped[int]
    calendar_year: Mapped[int]

    last_synced: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    @classmethod
    def convert_from_madden(cls, league_id: int, madden_hub_info: MaddenLeagueHubInfo):
        info = madden_hub_info.responseInfo.value
        return cls(
            league_id=league_id,
            calendar_year=info.careerHubInfo.seasonInfo.calendarYear,
            week=info.careerHubInfo.seasonInfo.displayWeek,
        )
