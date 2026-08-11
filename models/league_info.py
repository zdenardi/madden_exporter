from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column

from data_classes.madden_classes import MaddenLeagueInfo
from models.helper_classes import Base


class LeagueInfo(Base):
    __tablename__ = "league_info"
    league_id: Mapped[int] = mapped_column(primary_key=True)
    calendar_year: Mapped[int]
    week: Mapped[int]

    last_synced: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    @classmethod
    def convert_from_madden(cls, info: MaddenLeagueInfo):
        week = int(info["seasonText"].split()[-1])
        return cls(
            league_id=info["leagueId"],
            calendar_year=info["calendarYear"],
            week=week,
        )
