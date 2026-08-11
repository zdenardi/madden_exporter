from datetime import datetime, timezone

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.helper_classes import Base
from models.league_hub_info import LeagueHubInfo


class StatUpdate(Base):
    __tablename__ = "stat_update"
    __table_args__ = (
        UniqueConstraint(
            "league_info_id",
            "week_index",
            "stage_index",
            "calendar_year",
            name="_stat_update_uc",
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True)

    league_info_id: Mapped[int] = mapped_column(
        ForeignKey("league_hub_info.league_id"), nullable=False
    )

    week_index: Mapped[int]
    stage_index: Mapped[int]
    calendar_year: Mapped[int]
    league_id: Mapped[int]
    did_game_stat_sync: Mapped[bool] = mapped_column(default=False)
    did_players_sync: Mapped[bool] = mapped_column(default=False)
    did_passing_stat_sync: Mapped[bool] = mapped_column(default=False)
    did_rushing_stat_sync: Mapped[bool] = mapped_column(default=False)
    did_receiving_stat_sync: Mapped[bool] = mapped_column(default=False)
    did_defense_stat_sync: Mapped[bool] = mapped_column(default=False)
    did_punt_stat_sync: Mapped[bool] = mapped_column(default=False)
    did_kick_stat_sync: Mapped[bool] = mapped_column(default=False)

    league_hub_info: Mapped["LeagueHubInfo"] = relationship(
        back_populates="stat_updates"
    )

    last_synced: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
