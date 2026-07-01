from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


from models.helper_classes import Base

if TYPE_CHECKING:
    from models.TeamInfo import TeamInfo


class TeamStats(Base):
    __tablename__ = "team_stats"

    __table_args__ = (UniqueConstraint("team_id", "season", "week"),)

    id: Mapped[int] = mapped_column(primary_key=True)

    team_id: Mapped[int] = mapped_column(ForeignKey("team_infos.team_id"))
    season: Mapped[int]
    week: Mapped[int]

    wins: Mapped[int]
    losses: Mapped[int]

    points_for: Mapped[int]
    points_against: Mapped[int]
    standings_rank: Mapped[int]

    yards: Mapped[int]

    turnovers: Mapped[int]
    team: Mapped["TeamInfo"] = relationship(back_populates="stats")
