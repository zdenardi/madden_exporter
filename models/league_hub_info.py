from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from data_classes.madden_classes import MaddenLeagueHubInfo
from models.helper_classes import Base

if TYPE_CHECKING:
    from models.stat_update import StatUpdate


class LeagueHubInfo(Base):
    __tablename__ = "league_hub_info"
    league_id: Mapped[int] = mapped_column(primary_key=True)
    week: Mapped[int]
    calendar_year: Mapped[int]
    summaries: Mapped[str] = mapped_column(default="")
    stat_updates: Mapped[list["StatUpdate"]] = relationship(
        back_populates="league_hub_info",
        cascade="all, delete-orphan",
    )

    last_synced: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    @classmethod
    def convert_from_madden(cls, league_id: int, madden_hub_info: MaddenLeagueHubInfo):
        info = madden_hub_info.responseInfo.value
        game_summaries = madden_hub_info.responseInfo.value.get_human_game_summaries()
        summaries = "User Games: \n"
        for summary in game_summaries:
            summaries += f"   {summary['user_name']}: {summary['summary']} \n"
        return cls(
            league_id=league_id,
            calendar_year=info.careerHubInfo.seasonInfo.calendarYear,
            week=info.careerHubInfo.seasonInfo.displayWeek,
            summaries=summaries,
        )
