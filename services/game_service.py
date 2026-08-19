from sqlalchemy import select
from sqlalchemy.orm import Session

from app import EATokenInfo
from data_classes.data_classes import BlazeSession, TokenInformation, WeekInformation
from data_classes.madden_classes import MaddenScheduleEntry
from models.game import Game
from models.team_info import TeamInfo
from services.madden_data_service import (
    get_defensive_stats,
    get_kicking_stats,
    get_passing_stats,
    get_punting_stats,
    get_receiving_stats,
    get_rushing_stats,
    get_weekly_schedule,
)
from services.stat_services import (
    upsert_def,
    upsert_kick,
    upsert_pass,
    upsert_punt,
    upsert_rec,
    upsert_rush,
)


def upsert_game(session: Session, entry: MaddenScheduleEntry):
    stmt = select(Game).where(
        Game.week_index == entry.weekIndex,
        Game.away_team_id == entry.awayTeamId,
        Game.home_team_id == entry.homeTeamId,
        Game.schedule_id == entry.scheduleId,
    )

    game = session.execute(stmt).scalar_one_or_none()

    if game:
        game.away_score = entry.awayScore
        game.home_score = entry.homeScore
        game.schedule_id = entry.scheduleId
        game.week_index = entry.weekIndex
        game.status = entry.status
        game.season_index = entry.seasonIndex
        game.away_team_id = entry.awayTeamId
        game.home_team_id = entry.homeTeamId
    else:
        game = Game(
            away_score=entry.awayScore,
            home_score=entry.homeScore,
            season_index=entry.seasonIndex,
            schedule_id=entry.scheduleId,
            week_index=entry.weekIndex,
            status=entry.status,
            away_team_id=entry.awayTeamId,
            home_team_id=entry.homeTeamId,
        )
    session.add(game)
    session.flush()
    return game


def get_games_by_week(
    session: Session, week_index: int, season_index: int
) -> list[Game]:
    stmt = select(Game).where(
        Game.week_index == week_index, Game.season_index == season_index
    )

    games = session.execute(stmt).scalars().all()
    return games


def is_upset(game: Game) -> bool:

    winner = get_winner(game)
    favorite = get_favorite(game)
    if winner.team_id is not favorite.team_id:
        print("Upset Alert! \r")
        return True
    return False


def get_winner(game: Game):
    winner = (
        game.away_team
        if game.away_score > game.home_score
        else (game.home_team if game.home_score > game.away_score else None)
    )
    return winner


def get_favorite(game: Game) -> TeamInfo:
    return max(
        [game.home_team, game.away_team],
        key=lambda team: team.ovr_rating,
    )


def sync_games(
    token: EATokenInfo,
    blaze_session: BlazeSession,
    league_id: int,
    session: Session,
    week_info: WeekInformation,
):
    week = week_info.week_index - 1
    schedule = get_weekly_schedule(
        token, blaze_session, league_id, week_info.stage_index, week
    )
    for g in schedule:
        upsert_game(session, g)

    session.flush()

    passing_stats = get_passing_stats(
        token,
        blaze_session,
        league_id,
        week_info.stage_index,
        week_info.week_index - 1,
    )
    for stat in passing_stats:
        upsert_pass(session, stat)

    rushing_stats = get_rushing_stats(
        token,
        blaze_session,
        league_id,
        week_info.stage_index,
        week_info.week_index - 1,
    )
    for stat in rushing_stats:
        upsert_rush(session, stat)

    rec_stats = get_receiving_stats(
        token,
        blaze_session,
        league_id,
        week_info.stage_index,
        week_info.week_index - 1,
    )
    for stat in rec_stats:
        upsert_rec(session, stat)

    def_stats = get_defensive_stats(
        token,
        blaze_session,
        league_id,
        week_info.stage_index,
        week_info.week_index - 1,
    )
    for stat in def_stats:
        upsert_def(session, stat)

    punt_stats = get_punting_stats(
        token,
        blaze_session,
        league_id,
        week_info.stage_index,
        week_info.week_index - 1,
    )
    for stat in punt_stats:
        upsert_punt(session, stat)

    kicking_stats = get_kicking_stats(
        token,
        blaze_session,
        league_id,
        week_info.stage_index,
        week_info.week_index - 1,
    )
    for stat in kicking_stats:
        upsert_kick(session, stat)
