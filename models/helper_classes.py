from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, declarative_mixin, mapped_column


class Base(DeclarativeBase):
    pass


"""
This mixin is used for all "Stat" tables. All _stats share the same fields of 
- game_id 
- roster_id
- team_id
- season
- week
- stage

"""


@declarative_mixin
class StatMixin:
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    roster_id: Mapped[int] = mapped_column(
        ForeignKey("players.roster_id")
    )  # I believe maddens UUID for player
    team_id: Mapped[int] = mapped_column(ForeignKey("team_infos.team_id"))

    season: Mapped[int]
    week: Mapped[int]
    stage: Mapped[int]
