from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.helper_classes import Base

if TYPE_CHECKING:
    from models.Game import Game
    from models.TeamStats import TeamStats
    from models.Player import Player
    from models.TeamGameSummary import TeamGameSummary


class TeamInfo(Base):
    __tablename__ = "team_infos"

    team_id: Mapped[int] = mapped_column(primary_key=True)

    abbr_name: Mapped[str]
    city_name: Mapped[str]
    display_name: Mapped[str]
    injury_count: Mapped[int]
    nick_name: Mapped[str]
    ovr_rating: Mapped[int]
    primary_color: Mapped[int]
    secondary_color: Mapped[int]
    stats: Mapped[list["TeamStats"]] = relationship(back_populates="team")
    roster: Mapped[list["Player"]] = relationship(back_populates="team")
    home_games: Mapped[list["Game"]] = relationship(
        foreign_keys="Game.home_team_id",
        back_populates="home_team",
    )
    away_games: Mapped[list["Game"]] = relationship(
        foreign_keys="Game.away_team_id",
        back_populates="away_team",
    )

    game_summaries: Mapped[list["TeamGameSummary"]] = relationship(
        foreign_keys="TeamGameSummary.team_id",
        back_populates="team",
    )
