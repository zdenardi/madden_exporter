from sqlalchemy import JSON, Engine, UniqueConstraint, create_engine, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declarative_mixin,
    mapped_column,
    relationship,
    sessionmaker,
)

DATABASE_URL = "postgresql+psycopg://" "madden:madden@localhost:5432/madden"

engine = create_engine(
    DATABASE_URL,
    echo=False,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


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


class TeamStats(Base):
    __tablename__ = "team_stats"

    __table_args__ = (UniqueConstraint("team_id", "season", "week"),)

    id: Mapped[int] = mapped_column(primary_key=True)

    team_id: Mapped[int] = mapped_column(ForeignKey("team_infos.team_id"))
    season: Mapped[int]
    week: Mapped[int]

    wins: Mapped[int]
    losses: Mapped[int]

    points_for: Mapped[int]
    points_against: Mapped[int]
    standings_rank: Mapped[int]

    yards: Mapped[int]

    turnovers: Mapped[int]
    team: Mapped["TeamInfo"] = relationship(back_populates="stats")


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


class ReceivingStat(StatMixin, Base):
    __tablename__ = "receiving_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    rec_catches: Mapped[int]
    rec_catch_pct: Mapped[float]
    rec_drops: Mapped[int]
    rec_longest: Mapped[int]
    rec_pts: Mapped[int]
    rec_tds: Mapped[int]
    rec_to_pct: Mapped[float]
    rec_yds_after_catch: Mapped[int]
    rec_yac_per_catch: Mapped[int]
    rec_yds: Mapped[int]
    rec_yds_per_catch: Mapped[float]
    rec_yds_per_game: Mapped[float]

    game: Mapped["Game"] = relationship(back_populates="receiving_stats")


class RushingStat(StatMixin, Base):
    __tablename__ = "rushing_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    rush_att: Mapped[int]
    rush_broken_tackles: Mapped[int]
    rush_fum: Mapped[int]
    rush_longest: Mapped[int]
    rush_to_pct: Mapped[float]
    rush_tds: Mapped[int]
    rush_20_plus_yards: Mapped[int]
    rush_yds_after_contact: Mapped[int]
    rush_yds: Mapped[int]
    rush_yds_per_att: Mapped[float]
    rush_yds_per_game: Mapped[float]

    game: Mapped["Game"] = relationship(back_populates="rushing_stats")


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


class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[str]
    season: Mapped[int]
    week: Mapped[int]
    payload: Mapped[dict] = mapped_column(JSON)


class Game(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(primary_key=True)

    away_score: Mapped[int]
    home_score: Mapped[int]
    schedule_id: Mapped[int]  ## I believe this is maddens UUID for game
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


def setup_db(engine: Engine):
    Base.metadata.create_all(engine)
