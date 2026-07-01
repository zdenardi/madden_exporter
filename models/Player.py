from typing import TYPE_CHECKING

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.helper_classes import Base

if TYPE_CHECKING:
    from models.TeamInfo import TeamInfo


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

    team_id: Mapped[int] = mapped_column(ForeignKey("team_infos.team_id"))
