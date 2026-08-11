from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.helper_classes import Base, StatMixin

if TYPE_CHECKING:
    from models.Game import Game


class KickingStat(StatMixin, Base):
    __tablename__ = "kicking_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    kick_pts: Mapped[int]
    fg_att: Mapped[int]
    fg_50_plus_att: Mapped[int]
    fg_50_plus_made: Mapped[int]
    fg_longest: Mapped[int]
    fg_made: Mapped[int]
    fg_comp_pct: Mapped[float]
    kick_off_att: Mapped[int]
    kick_off_tbs: Mapped[int]
    xp_att: Mapped[int]
    xp_made: Mapped[int]
    xp_comp_pct: Mapped[float]

    game: Mapped["Game"] = relationship(back_populates="kicking_stats")
