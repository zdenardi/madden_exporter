from models import Game
from models.madden_classes import MaddenScheduleEntry
from services.game_services import (
    get_favorite,
    get_games_by_week,
    get_winner,
    upsert_game,
)


def test_upsert_game_creates_game(session, team_1, team_2):
    assert session.query(Game).count() == 0

    madden_sched_entry = MaddenScheduleEntry(
        awayScore=7,
        awayTeamId=team_1.team_id,
        isGameOfTheWeek=False,
        homeScore=3,
        homeTeamId=team_2.team_id,
        scheduleId=123,
        stageIndex=1,
        status=3,
        weekIndex=4,
        seasonIndex=1,
    )

    upsert_game(session, madden_sched_entry)
    assert session.query(Game).count() == 1


def test_upsert_game_updates_game(session, game):
    assert session.query(Game).count() == 1

    madden_sched_entry = MaddenScheduleEntry(
        awayScore=7,
        awayTeamId=game.away_team_id,
        isGameOfTheWeek=False,
        homeScore=3,
        homeTeamId=game.home_team_id,
        scheduleId=game.schedule_id,
        stageIndex=1,
        status=3,
        weekIndex=game.week_index,
        seasonIndex=1,
    )

    updated_game = upsert_game(session, madden_sched_entry)
    session.flush()
    assert updated_game.id == game.id
    assert updated_game.home_score == madden_sched_entry.homeScore
    assert updated_game.away_score == madden_sched_entry.awayScore


def test_get_games_by_week(session, game):
    games = get_games_by_week(session, game.week_index, game.season_index)
    assert len(games) == 1
    assert games[0] == game


def test_get_winner(session, game):
    winner = get_winner(game)
    assert winner == game.home_team


def test_get_fav(session, game):
    fav = get_favorite(game)
    assert fav == game.away_team
