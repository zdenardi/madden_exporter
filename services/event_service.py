from db import Event, Game
from services.game_services import get_favorite


def create_upset_event(game: Game):
    favorite = get_favorite(game)
    underdog = (
        game.away_team if favorite.team_id == game.home_team.team_id else game.home_team
    )

    return Event(
        event_type="UPSET",
        season=game.season_index,
        week=game.week_index,
        payload={
            "game": {
                "rating_difference": (favorite.ovr_rating - underdog.ovr_rating),
                "id": game.id,
                "season": game.season_index,
                "week": game.week_index,
                "away_team": game.away_team.display_name,
                "away_score": game.away_score,
                "home_team": game.home_team.display_name,
                "home_score": game.home_score,
                "favorite": favorite.display_name,
                "underdog": underdog.display_name,
            }
        },
    )
