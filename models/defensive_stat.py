from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.helper_classes import Base, StatMixin

if TYPE_CHECKING:
    from Game import Game


class DefensiveStat(StatMixin, Base):
    __tablename__ = "defensive_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    def_catch_allowed: Mapped[int]
    def_deflections: Mapped[int]
    def_forced_fum: Mapped[int]
    def_fum_rec: Mapped[int]
    def_ints: Mapped[int]
    def_int_return_yds: Mapped[int]
    def_pts: Mapped[int]
    def_sacks: Mapped[float]
    def_safeties: Mapped[int]
    def_tds: Mapped[int]
    def_total_tackles: Mapped[int]

    game: Mapped["Game"] = relationship(back_populates="defensive_stats")
