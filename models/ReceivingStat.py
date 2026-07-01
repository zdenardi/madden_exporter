from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.helper_classes import Base, StatMixin

if TYPE_CHECKING:
    from models.Game import Game


class ReceivingStat(StatMixin, Base):
    __tablename__ = "receiving_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    rec_catches: Mapped[int]
    rec_catch_pct: Mapped[float]
    rec_drops: Mapped[int]
    rec_longest: Mapped[int]
    rec_pts: Mapped[int]
    rec_tds: Mapped[int]
    rec_to_pct: Mapped[float]
    rec_yds_after_catch: Mapped[int]
    rec_yac_per_catch: Mapped[int]
    rec_yds: Mapped[int]
    rec_yds_per_catch: Mapped[float]
    rec_yds_per_game: Mapped[float]

    game: Mapped["Game"] = relationship(back_populates="receiving_stats")
