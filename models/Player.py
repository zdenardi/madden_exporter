from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.helper_classes import Base

if TYPE_CHECKING:
    from models import (
        DefensiveStat,
        KickingStat,
        PassingStat,
        PuntingStat,
        ReceivingStat,
        RushingStat,
    )
    from models.team_info import TeamInfo


class Player(Base):
    __tablename__ = "players"
    roster_id: Mapped[int] = mapped_column(primary_key=True)
    age: Mapped[int]
    college: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    position: Mapped[str]
    is_active: Mapped[bool]
    jersey_num: Mapped[int]
    years_pro: Mapped[int]
    ratings: Mapped[dict] = mapped_column(JSONB)

    team: Mapped["TeamInfo"] = relationship(back_populates="roster")
    passing_stats: Mapped[list["PassingStat"]] = relationship(back_populates="player")
    defensive_stats: Mapped[list["DefensiveStat"]] = relationship(
        back_populates="player"
    )
    rushing_stats: Mapped[list["RushingStat"]] = relationship(back_populates="player")
    kicking_stats: Mapped[list["KickingStat"]] = relationship(back_populates="player")
    punting_stats: Mapped[list["PuntingStat"]] = relationship(back_populates="player")
    receiving_stats: Mapped[list["ReceivingStat"]] = relationship(
        back_populates="player"
    )

    team_id: Mapped[int] = mapped_column(ForeignKey("team_infos.team_id"))
