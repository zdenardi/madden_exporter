from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from models.helper_classes import Base

if TYPE_CHECKING:
    from models.TeamGameSummary import TeamGameSummary
    from models.TeamInfo import TeamInfo
    from models.DefensiveStat import DefensiveStat
    from models.KickingStat import KickingStat
    from models.PassingStat import PassingStat
    from models.PuntingStat import PuntingStat
    from models.ReceivingStat import ReceivingStat
    from models.RushingStat import RushingStat


class Game(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(primary_key=True)

    away_score: Mapped[int]
    home_score: Mapped[int]
    schedule_id: Mapped[int]  # I believe this is maddens UUID for game
    week_index: Mapped[int]
    summaries: Mapped[list["TeamGameSummary"]] = relationship(
        foreign_keys="TeamGameSummary.game_id",
        back_populates="game",
    )
    status: Mapped[int]
    season_index: Mapped[int]

    away_team_id: Mapped[int] = mapped_column(ForeignKey("team_infos.team_id"))
    home_team_id: Mapped[int] = mapped_column(ForeignKey("team_infos.team_id"))

    away_team: Mapped["TeamInfo"] = relationship(
        foreign_keys=[away_team_id], back_populates="away_games"
    )
    home_team: Mapped["TeamInfo"] = relationship(
        foreign_keys=[home_team_id], back_populates="home_games"
    )

    passing_stats: Mapped[list["PassingStat"]] = relationship(back_populates="game")
    rushing_stats: Mapped[list["RushingStat"]] = relationship(back_populates="game")
    receiving_stats: Mapped[list["ReceivingStat"]] = relationship(back_populates="game")
    defensive_stats: Mapped[list["DefensiveStat"]] = relationship(back_populates="game")
    kicking_stats: Mapped[list["KickingStat"]] = relationship(back_populates="game")
    punting_stats: Mapped[list["PuntingStat"]] = relationship(back_populates="game")
