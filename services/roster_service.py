from sqlalchemy import select
from sqlalchemy.orm import Session

from db import Player
from madden_classes import MaddenPlayerData


def upsert_player(session: Session, p: MaddenPlayerData):
    PLAYER_FIELDS = {
        "age",
        "firstName",
        "lastName",
        "position",
        "isActive",
        "jerseyNum",
        "yearsPro",
        "rosterId",
        "teamId",
        "college",
    }

    player = p.model_dump()

    ratings = {key: value for key, value in player.items() if key not in PLAYER_FIELDS}

    stmt = select(Player).where(Player.roster_id == player["rosterId"])
    existing = session.execute(stmt).scalar_one_or_none()
    if existing:
        existing.age = player["age"]
        existing.college = player["college"]
        existing.first_name = player["firstName"]
        existing.last_name = player["lastName"]
        existing.position = player["position"]
        existing.is_active = player["isActive"]
        existing.jersey_num = player["jerseyNum"]
        existing.years_pro = player["yearsPro"]
        existing.team_id = player["teamId"]
        existing.ratings = ratings
        return False, existing
    else:
        player = Player(
            roster_id=player["rosterId"],
            age=player["age"],
            college=player["college"],
            first_name=player["firstName"],
            last_name=player["lastName"],
            position=player["position"],
            is_active=player["isActive"],
            jersey_num=player["jerseyNum"],
            years_pro=player["yearsPro"],
            team_id=player["teamId"],
            ratings=ratings,
        )
        session.add(player)
        return True, player
