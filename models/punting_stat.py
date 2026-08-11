from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.helper_classes import Base, StatMixin

if TYPE_CHECKING:
    from models.Game import Game


class PuntingStat(StatMixin, Base):
    __tablename__ = "punting_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    punt_blocked: Mapped[int]
    punts_in_20: Mapped[int]
    punt_longest: Mapped[int]
    punt_tbs: Mapped[int]
    punt_net_yds_per_att: Mapped[float]
    punt_net_yds: Mapped[int]
    punt_att: Mapped[int]
    punt_yds_per_att: Mapped[float]
    punt_yds: Mapped[int]

    game: Mapped["Game"] = relationship(back_populates="punting_stats")
