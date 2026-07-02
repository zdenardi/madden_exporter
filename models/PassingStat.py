from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.helper_classes import StatMixin, Base

if TYPE_CHECKING:
    from models.Game import Game


class PassingStat(StatMixin, Base):
    __tablename__ = "passing_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    pass_att: Mapped[int]
    pass_comp: Mapped[int]
    pass_comp_pct: Mapped[float]
    pass_ints: Mapped[int]
    pass_longest: Mapped[int]
    pass_pts: Mapped[int]
    passer_rating: Mapped[float]
    pass_sacks: Mapped[int]
    pass_tds: Mapped[int]
    pass_yds: Mapped[int]
    pass_yds_per_att: Mapped[float]
    pass_yds_per_game: Mapped[float]

    game: Mapped["Game"] = relationship(back_populates="passing_stats")
