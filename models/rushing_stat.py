from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.helper_classes import Base, StatMixin

if TYPE_CHECKING:
    from models.Game import Game


class RushingStat(StatMixin, Base):
    __tablename__ = "rushing_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    rush_att: Mapped[int]
    rush_broken_tackles: Mapped[int]
    rush_fum: Mapped[int]
    rush_longest: Mapped[int]
    rush_to_pct: Mapped[float]
    rush_tds: Mapped[int]
    rush_20_plus_yards: Mapped[int]
    rush_yds_after_contact: Mapped[int]
    rush_yds: Mapped[int]
    rush_yds_per_att: Mapped[float]
    rush_yds_per_game: Mapped[float]

    game: Mapped["Game"] = relationship(back_populates="rushing_stats")
