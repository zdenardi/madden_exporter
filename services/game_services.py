from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.Game import Game
from models.TeamInfo import TeamInfo
from models.madden_classes import MaddenScheduleEntry


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
    return game


def get_games_by_week(session: Session, week: int, season: int) -> List[Game]:
    stmt = select(Game).where(Game.week_index == week, Game.season_index == season)

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
