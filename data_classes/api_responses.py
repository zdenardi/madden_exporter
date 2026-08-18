from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class MaddenDataFromDB(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )


class TeamInfoResponse(MaddenDataFromDB):

    team_id: int
    city_name: str
    abbr_name: str
    nick_name: str


class PlayerResponse(MaddenDataFromDB):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )
    age: int
    college: str
    first_name: str
    last_name: str
    position: str
    is_active: bool
    jersey_num: int
    years_pro: int
    ratings: dict


class PlayerStat(MaddenDataFromDB):
    player: PlayerResponse


class Passing(PlayerStat):
    pass_att: int
    pass_comp: int
    pass_comp_pct: float
    pass_ints: int
    pass_longest: int
    pass_pts: int
    passer_rating: float
    pass_sacks: int
    pass_tds: int
    pass_yds: int
    pass_yds_per_att: float
    pass_yds_per_game: float
    player: PlayerResponse


class Rushing(PlayerStat):
    rush_att: int
    rush_broken_tackles: int
    rush_fum: int
    rush_longest: int
    rush_to_pct: float
    rush_tds: int
    rush_20_plus_yards: int
    rush_yds_after_contact: int
    rush_yds: int
    rush_yds_per_att: float
    rush_yds_per_game: float


class Receiving(PlayerStat):
    rec_catches: int
    rec_catch_pct: float
    rec_drops: int
    rec_longest: int
    rec_pts: int
    rec_tds: int
    rec_to_pct: float
    rec_yds_after_catch: int
    rec_yac_per_catch: int
    rec_yds: int
    rec_yds_per_catch: float
    rec_yds_per_game: float


class Defense(PlayerStat):
    def_catch_allowed: int
    def_deflections: int
    def_forced_fum: int
    def_fum_rec: int
    def_ints: int
    def_int_return_yds: int
    def_pts: int
    def_sacks: float
    def_safeties: int
    def_tds: int
    def_total_tackles: int


class Kicking(PlayerStat):
    kick_pts: int
    fg_att: int
    fg_50_plus_att: int
    fg_50_plus_made: int
    fg_longest: int
    fg_made: int
    fg_comp_pct: float
    kick_off_att: int
    kick_off_tbs: int
    xp_att: int
    xp_made: int
    xp_comp_pct: float


class Punting(PlayerStat):
    punt_blocked: int
    punts_in_20: int
    punt_longest: int
    punt_tbs: int
    punt_net_yds_per_att: float
    punt_net_yds: int
    punt_att: int
    punt_yds_per_att: float
    punt_yds: int


class TeamGameResponse(MaddenDataFromDB):

    team: TeamInfoResponse

    passing_stats: list[Passing]
    rushing_stats: list[Rushing]
    receiving_stats: list[Receiving]
    defensive_stats: list[Defense]
    kicking_stats: list[Kicking]
    punting_stats: list[Punting]


class GameResponse(MaddenDataFromDB):
    id: int
    away_score: int
    home_score: int
    away_team: TeamGameResponse
    home_team: TeamGameResponse
    status: str
