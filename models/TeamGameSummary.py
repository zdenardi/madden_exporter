from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Game, TeamInfo
from models.helper_classes import Base

if TYPE_CHECKING:
    from models.Game import Game
    from models.TeamInfo import TeamInfo


class TeamGameSummary(Base):
    __tablename__ = "madden_game_stats"
    __table_args__ = (UniqueConstraint("schedule_id", "team_id"),)
    stat_id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("team_infos.team_id"))
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))

    team: Mapped["TeamInfo"] = relationship(
        foreign_keys=[team_id], back_populates="game_summaries"
    )
    game: Mapped["Game"] = relationship(
        foreign_keys=[game_id], back_populates="summaries"
    )

    schedule_id: Mapped[int]

    week_index: Mapped[int]
    def_forced_fum: Mapped[int]
    def_fum_rec: Mapped[int]
    def_ints_rec: Mapped[int]
    def_pts_per_game: Mapped[float]
    def_pass_yds: Mapped[int]
    def_rush_yds: Mapped[int]
    def_red_zone_fgs: Mapped[int]
    def_red_zones: Mapped[int]
    def_red_zone_pct: Mapped[float]
    def_red_zone_tds: Mapped[int]
    def_sacks: Mapped[int]
    def_total_yds: Mapped[int]
    off_4th_down_att: Mapped[int]
    off_4th_down_conv: Mapped[int]
    off_4th_down_conv_pct: Mapped[float]
    off_fum_lost: Mapped[int]
    off_ints_lost: Mapped[int]
    off_1st_downs: Mapped[int]
    off_pts_per_game: Mapped[float]
    off_pass_tds: Mapped[int]
    off_pass_yds: Mapped[int]
    off_rush_tds: Mapped[int]
    off_rush_yds: Mapped[int]
    off_red_zone_fgs: Mapped[int]
    off_red_zones: Mapped[int]
    off_red_zone_pct: Mapped[float]
    off_red_zone_tds: Mapped[int]
    off_sacks: Mapped[int]
    off_3rd_down_att: Mapped[int]
    off_3rd_down_conv: Mapped[int]
    off_3rd_down_conv_pct: Mapped[float]
    off_2pt_att: Mapped[int]
    off_2pt_conv: Mapped[int]
    off_2pt_conv_pct: Mapped[float]
    off_total_yds: Mapped[int]
    off_total_yds_gained: Mapped[int]
    penalties: Mapped[int]
    penalty_yds: Mapped[int]
    seed: Mapped[int]
    season_index: Mapped[int]
    stage_index: Mapped[int]
    total_losses: Mapped[int]
    total_ties: Mapped[int]
    total_wins: Mapped[int]
    to_diff: Mapped[int]
    to_giveaways: Mapped[int]
    to_takeaways: Mapped[int]
