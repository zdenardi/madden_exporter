import json
import os
import random
import traceback
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request
from sqlalchemy import select

from constants import REDIRECT_URL
from data_classes.madden_classes import (
    MaddenKickingStat,
    MaddenPassingStat,
    MaddenPlayerData,
    MaddenPuntingStat,
    MaddenReceivingStat,
    MaddenRushingStat,
    MaddenScheduleEntry,
    MaddenStandingsEntry,
    MaddenTeam,
)
from db import SessionLocal, engine, setup_db
from models.EAtoken import EATokenInfo
from models.TeamInfo import TeamInfo
from services import slack_service
from services.ea_services import (
    LEAGUE_ID,
    get_blaze_session,
    get_EA_access_token,
    get_EA_jws_token,
    get_EA_token_info,
    get_madden_league_hub,
    get_persona_auth_code,
    get_personas,
    parse_qs,
)
from services.event_service import create_upset_event
from services.game_services import (
    get_games_by_week,
    is_upset,
    upsert_game,
)
from services.league_hub_info_service import LeagueHubInfoService
from services.roster_service import upsert_player
from services.stat_services import (
    upsert_kick,
    upsert_pass,
    upsert_punt,
    upsert_rec,
    upsert_rush,
    upsert_stat,
)
from services.team_services import upsert_team

load_dotenv()
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")
APP_ENV = os.getenv("APP_ENV")


app = Flask(__name__)
setup_db(engine)


@app.route("/")
def home():

    return {"status": "ok"}


@app.route("/<platform>/<league_id>/team/<team_id>/roster", methods=["POST"])
def import_weekly_roster(
    platform: str,  # xbsx
    league_id: str,
    team_id: str,
):
    session = SessionLocal()

    team = session.get(TeamInfo, int(team_id))
    if team is None:
        return {"error": "No team found!"}
    display_name = team.display_name
    data = request.get_json()
    players = data["rosterInfoList"]
    updated_players = 0
    created_players = 0
    try:
        for player in players:
            player = MaddenPlayerData.model_validate(player)
            created, p = upsert_player(session, player)
            if created:
                created_players += 1
            else:
                updated_players += 1

        session.commit()
    except Exception:
        session.rollback()
        traceback.print_exc()
    finally:
        session.close()

    filename = f"exports/" f"roster_{display_name}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved roster for {team_id}")
    print(f"Created {created_players} players and updated {updated_players}")

    return {"success": True}


@app.route("/<platform>/<league_id>/week/<type>/<num>/<resource>", methods=["POST"])
def import_schedule_stats(
    platform: str,  # xbsx
    league_id: str,
    type: str,  # reg post? pre?
    num: str,  # num of week,
    resource: str,  # schedule,receiving,rushing,defense,team,passing,kicking,punting
):
    session = SessionLocal()

    data = request.get_json()

    filename = f"exports/" f"{resource}_week_{num}_{type}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved week {num} {resource}")
    if resource == "passing":
        try:
            for stat in data["playerPassingStatInfoList"]:
                m_pass_stat = MaddenPassingStat.model_validate(stat)
                upsert_pass(session, m_pass_stat)
            session.commit()
        except Exception:
            session.rollback()
            traceback.print_exc()

        finally:
            session.close()

    if resource == "punting":
        try:
            for stat in data["playerPuntingStatInfoList"]:
                m_punt_stat = MaddenPuntingStat.model_validate(stat)
                upsert_punt(session, m_punt_stat)
            session.commit()
        except Exception:
            session.rollback()
            traceback.print_exc()

        finally:
            session.close()

    if resource == "receiving":
        try:
            for stat in data["playerReceivingStatInfoList"]:
                m_rec_stat = MaddenReceivingStat.model_validate(stat)
                upsert_rec(session, m_rec_stat)
            session.commit()
        except Exception:
            session.rollback()
            traceback.print_exc()

        finally:
            session.close()
    if resource == "rushing":
        try:
            for stat in data["playerRushingStatInfoList"]:
                m_rec_stat = MaddenRushingStat.model_validate(stat)
                upsert_rush(session, m_rec_stat)
            session.commit()
        except Exception:
            session.rollback()
            traceback.print_exc()

        finally:
            session.close()
    if resource == "kicking":
        try:
            for stat in data["playerKickingStatInfoList"]:
                m_kick_stat = MaddenKickingStat.model_validate(stat)
                upsert_kick(session, m_kick_stat)
            session.commit()
        except Exception:
            session.rollback()
            traceback.print_exc()

        finally:
            session.close()

    if resource == "schedules":
        try:
            for stat in data["gameScheduleInfoList"]:
                m_sched_stat = MaddenScheduleEntry.model_validate(stat)
                upsert_game(session, m_sched_stat)
            session.commit()
        except Exception:
            session.rollback()
            traceback.print_exc()

        finally:
            session.close()

    # if resource == "team":
    #     print("Trying to save team!")
    #     try:
    #         for stat in data["teamStatInfoList"]:
    #             m_game_stat = MaddenScheduleEntry.model_validate(stat)
    #             upsert_game(session, m_game_stat)
    #         session.commit()
    #     except Exception:
    #         session.rollback()
    #         traceback.print_exc()

    #     finally:
    #         session.close()

    return {"success": True}


@app.route("/<platform>/<league_id>/<resource>", methods=["POST"])
def import_resource(
    platform: str,
    league_id: str,
    resource: str,
):
    session = SessionLocal()

    data = request.get_json()

    filename = f"exports/" f"{platform}_{league_id}_{resource}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {resource}")
    if resource == "leagueteams":
        print("Saving league teams")
        try:
            for team in data["leagueTeamInfoList"]:
                team_info = MaddenTeam.model_validate(team)
                upsert_team(session, team_info)
            session.commit()
        except Exception:
            session.rollback()
            traceback.print_exc()
        finally:
            session.close()

    if resource == "standings":
        print("Saving standings")
        try:
            for team_stat in data["teamStandingInfoList"]:
                entry = MaddenStandingsEntry.model_validate(team_stat)
                upsert_stat(session, entry)
            session.commit()
        except Exception:
            session.rollback()
            traceback.print_exc()
        finally:
            session.close()

    return {"success": True}


# @app.route("/<path:path>", methods=["GET", "POST"])
# def catch_all(path):
#     print("PATH:", path)
#     print("METHOD:", request.method)

#     data = None
#     try:
#         data = request.get_json()
#     except Exception:
#         # This handles cases where content-type might be wrong or body is empty
#         pass

#     log_entry = {
#         "path": path,
#         "method": request.method,
#         "json_data": data,  # Will contain the parsed JSON or None if none was present/parsed
#     }

#     # Using a more descriptive filename that includes time and perhaps some unique ID
#     filename = f"exports/log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(path + request.method)}.json"

#     try:
#         with open(filename, "w") as f:
#             json.dump(log_entry, f, indent=2)
#     except Exception as e:
#         print(f"Error writing log file: {e}")

#     return {"received": path}


@app.route("/game/<int:season>/<int:week>", methods=["GET"])
def games():
    session = SessionLocal()

    games = get_games_by_week(session, 15, 12)

    for game in games:
        print(
            f"{game.away_team.display_name} "
            f"{game.away_score} - "
            f"{game.home_score} "
            f"{game.home_team.display_name} \r"
        )
        if is_upset(game):
            session.add(create_upset_event(game))
            session.commit()

    session.close()
    return {"success": True}


@app.route("/reddit", methods=["GET"])
def create_reddit_post():
    session = SessionLocal()
    games = get_games_by_week(session, 15, 12)

    events = []

    for game in games:
        if is_upset(game):
            event = create_upset_event(game)
            session.add(event)
            events.append(event)

    session.commit()
    cowboys_events = [event for event in events if "Cowboys" in str(event.payload)]

    if not events:
        return {"success": False, "message": "No upsets found"}

    # Pick a random upset
    cowboys_events = [event for event in events if "Cowboys" in str(event.payload)]
    event = random.choice(cowboys_events)
    print(f"""
        Event Type: {event.event_type}
        Season: {event.season}
        Week: {event.week}
        Payload:
        {event.payload}
        """)

    prompt = f"""
        Event:
        {event.payload}
        You are a Reddit NFL fan posting on r/nfl.

        React to this upset like a real Reddit user.
        Be opinionated, casual, and include some humor.
        Do not use actual NFL player names, use only positional groups like WR, or QB, Secondary, Offense, Etc.
        You can use the NFL team names and the city where they are

        Write a Reddit post title and a short comment.
        Use the event.favorite as the team that should have won and the event.underdog the team who should have lost
        """

    prompt2 = f"""
        Event:
        {event.payload}
        You are an ESPN Writer

        Do not use actual NFL player names, use only positional groups like WR, or QB, Secondary, Offense, Etc.
        You can use the NFL team names and the city where they are

        Write an article blurb about this game.
        Use the event.favorite as the team that should have won but lost, and the event.underdog the team who should have lost but won
        """

    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "llama3.1:8b",
            "prompt": prompt2,
            "stream": False,
        },
    )

    data = response.json()

    print(data["response"])

    return {
        "success": True,
        "event": event.payload,
        "reddit_post": data["response"],
    }


@app.route("/sync_league", methods=["GET"])
def sync_league():
    channel_name = "madden3" if APP_ENV == "prod" else "test_madden_bot"
    session = SessionLocal()
    token = get_EA_token_info(session)
    blaze_session = get_blaze_session(token)
    league_info = get_madden_league_hub(token, blaze_session)
    week_info = LeagueHubInfoService.get_week_info(session, league_info, LEAGUE_ID)
    if week_info.was_created:
        slack_service.send_message("Tracking League Advancement!", channel_name)
        slack_service.send_message(week_info.summaries, channel_name)

    if week_info.week_changed:
        slack_service.send_message(
            f"Week has advanced from Week {week_info.old_week} to {week_info.current_week}",
            channel_name,
        )

    if week_info.season_changed:
        slack_service.send_message(
            f"Season has advanced from Week {week_info.old_year} to {week_info.current_year}",
            channel_name,
        )
        slack_service.send_message(week_info.summaries, channel_name)

    if week_info.did_summaries_update:
        slack_service.send_message(week_info.summaries, channel_name)

    try:
        session.commit()
    finally:
        session.close()

    return {"success": True}


@app.route("/login_EA", methods=["GET"])
def get_auth_code_from_url():
    return render_template("get_auth_code.html")


@app.route("/submit_url", methods=["POST"])
def get_code_from_url():
    session = SessionLocal()

    url = request.form.get("url")

    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    code = query_params.get("code", [""])[0]
    token = get_EA_access_token(code)
    personas = get_personas(token)
    persona = personas[0]
    p_code = get_persona_auth_code(token["access_token"], persona)
    ea_jws = get_EA_jws_token(p_code)
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=ea_jws["expires_in"])
    token_info = EATokenInfo(
        access_token=ea_jws["access_token"],
        refresh_token=ea_jws["refresh_token"],
        expires_at=expires_at,
    )
    blaze_session = get_blaze_session(token_info)
    league_info = get_madden_league_hub(token_info, blaze_session)
    if (
        league_info.responseInfo.tdfclass
        == "Blaze::FranchiseMode::MobileCareer::GetLeagueHubResponse"
    ):
        token = session.scalar(statement=select(EATokenInfo))
        if token is None:
            session.add(token_info)

        else:
            token.access_token = token_info.access_token
            token.refresh_token = token_info.refresh_token
            token.expires_at = token_info.expires_at
        try:
            session.commit()
        finally:
            session.close()
        return {"success": True, "token": "Valid"}
    else:
        return {"success": False}
