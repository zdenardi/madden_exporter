from constants import (
    LEAGUE_ID,
)
from data_classes.data_classes import (
    BlazeSession,
    TokenInformation,
)
from data_classes.madden_classes import (
    MaddenDefensiveStat,
    MaddenKickingStat,
    MaddenLeagueHubInfo,
    MaddenLeagueInfo,
    MaddenPassingStat,
    MaddenPlayerData,
    MaddenPuntingStat,
    MaddenReceivingStat,
    MaddenRushingStat,
    MaddenScheduleEntry,
    MaddenStandingsEntry,
    MaddenTeam,
    MaddenTeamStat,
)
from services.ea_auth_service import get_export_data, send_blaze_req


def get_madden_league_info(token: TokenInformation, blaze_session: BlazeSession):
    response = send_blaze_req(
        token,
        blaze_session,
        {
            "commandName": "Mobile_GetMyLeagues",
            "componentId": 2060,
            "commandId": 801,
            "requestPayload": {},
            "componentName": "careermode",
        },
    )
    if response.ok and response.json()["responseInfo"]:
        league_info: MaddenLeagueInfo = response.json()["responseInfo"]["value"][
            "leagues"
        ][0]

        return league_info
    else:
        print(response.json())
        raise Exception("Error getting leagues")


def get_madden_league_hub(token: TokenInformation, blaze_session: BlazeSession):
    response = send_blaze_req(
        token,
        blaze_session,
        {
            "commandName": "Mobile_Career_GetLeagueHub",
            "componentId": 2060,
            "commandId": 811,
            "requestPayload": {"leagueId": LEAGUE_ID},
            "componentName": "careermode",
        },
    )
    if (
        response.ok
        and response.json()["responseInfo"]["tdfclass"]
        == "Blaze::FranchiseMode::MobileCareer::GetLeagueHubResponse"
    ):
        json = response.json()
        league_hub_info = MaddenLeagueHubInfo.model_validate(json)
        return league_hub_info
    else:
        print(response.json())
        raise Exception("Error getting leagues")


def get_teams(token: TokenInformation, blaze_session: BlazeSession, league_id: int):
    response = get_export_data(token, blaze_session, "TEAMS", {"leagueId": LEAGUE_ID})
    if response.ok and response.json()["leagueTeamInfoList"]:
        data = response.json()
        try:
            return [
                MaddenTeam.model_validate(team) for team in data["leagueTeamInfoList"]
            ]
        except KeyError:
            raise Exception("TEAMS response missing leagueTeamInfoList")

    else:
        raise Exception["Error getting teams"]


def get_standings(token: TokenInformation, blaze_session: BlazeSession, league_id: int):
    response = get_export_data(
        token, blaze_session, "STANDINGS", {"leagueId": LEAGUE_ID}
    )
    if response.ok and response.json()["teamStandingInfoList"]:
        standings: list[MaddenStandingsEntry] = response.json()["teamStandingInfoList"]
        return standings
    else:
        raise Exception["Error getting standings"]


def get_weekly_schedule(
    token: TokenInformation,
    blaze_session: BlazeSession,
    league_id: int,
    stage_index: int,
    weekly_index: int,
):
    response = get_export_data(
        token,
        blaze_session,
        "WEEKLY_SCHEDULE",
        {"leagueId": LEAGUE_ID, "stageIndex": stage_index, "weeklyIndex": weekly_index},
    )
    if response.ok and response.json()["gameScheduleInfoList"]:
        data = response.json()
        try:
            return [
                MaddenScheduleEntry.model_validate(game)
                for game in data["gameScheduleInfoList"]
            ]
        except KeyError:
            raise Exception("Game missing from gameScheduleInfoList")
        weekly_schedule: list[MaddenScheduleEntry] = response.json()[
            "gameScheduleInfoList"
        ]
        return weekly_schedule
    else:
        raise Exception["Error getting weekly schedule"]


def get_rushing_stats(
    token: TokenInformation,
    session: BlazeSession,
    league_id: int,
    stage_index: int,
    week_index: int,
):
    response = get_export_data(
        token,
        session,
        "RUSHING_STATS",
        {"leagueId": LEAGUE_ID, "stageIndex": stage_index, "week_index": week_index},
    )
    if response.ok and response.json()["playerRushingStatInfoList"]:
        stats: list[MaddenRushingStat] = response.json()["playerRushingStatInfoList"]
        return stats
    else:
        raise Exception[
            f"Error getting Rushing Stats for Stage:{stage_index}, Week:{week_index}"
        ]


def get_passing_stats(
    token: TokenInformation,
    session: BlazeSession,
    league_id: int,
    stage_index: int,
    week_index: int,
) -> list[MaddenPassingStat]:
    response = get_export_data(
        token,
        session,
        "PASSING_STATS",
        {"leagueId": LEAGUE_ID, "stageIndex": stage_index, "week_index": week_index},
    )
    if response.ok and response.json()["playerPassingStatInfoList"]:
        stats: list[MaddenPassingStat] = response.json()["playerPassingStatInfoList"]
        return stats
    else:
        raise Exception[
            f"Error getting Passing Stats for Stage:{stage_index}, Week:{week_index}"
        ]


def get_punting_stats(
    token: TokenInformation,
    session: BlazeSession,
    league_id: int,
    stage_index: int,
    week_index: int,
) -> list[MaddenPuntingStat]:
    response = get_export_data(
        token,
        session,
        "PUNTING_STATS",
        {"leagueId": LEAGUE_ID, "stageIndex": stage_index, "week_index": week_index},
    )
    if response.ok and response.json()["playerPuntingStatInfoList"]:
        stats: list[MaddenPuntingStat] = response.json()["playerPuntingStatInfoList"]
        return stats
    else:
        raise Exception[
            f"Error getting Passing Stats for Stage:{stage_index}, Week:{week_index}"
        ]


def get_receiving_stats(
    token: TokenInformation,
    session: BlazeSession,
    league_id: int,
    stage_index: int,
    week_index: int,
) -> list[MaddenReceivingStat]:
    response = get_export_data(
        token,
        session,
        "RECEIVING_STATS",
        {"leagueId": LEAGUE_ID, "stageIndex": stage_index, "week_index": week_index},
    )
    if response.ok and response.json()["playerReceivingStatInfoList"]:
        stats: list[MaddenReceivingStat] = response.json()[
            "playerReceivingStatInfoList"
        ]
        return stats
    else:
        raise Exception[
            f"Error getting Passing Stats for Stage:{stage_index}, Week:{week_index}"
        ]


def get_defensive_stats(
    token: TokenInformation,
    session: BlazeSession,
    league_id: int,
    stage_index: int,
    week_index: int,
) -> list[MaddenDefensiveStat]:
    response = get_export_data(
        token,
        session,
        "DEFENSIVE_STATS",
        {"leagueId": LEAGUE_ID, "stageIndex": stage_index, "week_index": week_index},
    )
    if response.ok and response.json()["playerDefensiveStatInfoList"]:
        stats: list[MaddenDefensiveStat] = response.json()[
            "playerDefensiveStatInfoList"
        ]
        return stats
    else:
        raise Exception[
            f"Error getting Passing Stats for Stage:{stage_index}, Week:{week_index}"
        ]


def get_kicking_stats(
    token: TokenInformation,
    session: BlazeSession,
    league_id: int,
    stage_index: int,
    week_index: int,
) -> list[MaddenKickingStat]:
    response = get_export_data(
        token,
        session,
        "KICKING_STATS",
        {"leagueId": LEAGUE_ID, "stageIndex": stage_index, "week_index": week_index},
    )
    if response.ok and response.json()["playerKickingStatInfoList"]:
        stats: list[MaddenKickingStat] = response.json()["playerKickingStatInfoList"]
        return stats
    else:
        raise Exception[
            f"Error getting Passing Stats for Stage:{stage_index}, Week:{week_index}"
        ]


def get_team_roster(
    token: TokenInformation,
    blaze_session: BlazeSession,
    league_id: int,
    team_id: int,
) -> list[MaddenPlayerData]:
    response = get_export_data(
        token,
        blaze_session,
        "TEAM_ROSTER",
        {
            "leagueId": LEAGUE_ID,
            "teamId": team_id,
            "returnFreeAgents": False,
        },
    )
    if response.ok and response.json()["rosterInfoList"]:
        data = response.json()
        try:
            return [
                MaddenPlayerData.model_validate(player)
                for player in data["rosterInfoList"]
            ]
        except KeyError:
            raise Exception("PLAYER response missing rosterInfoList")
    else:
        raise Exception[f"Error getting Team roster for {team_id}"]


def get_team_stats(
    token: TokenInformation,
    blaze_session: BlazeSession,
    league_id: int,
    stage: int,  # preseason 0, season 1
    week_index: int,
) -> list[MaddenTeamStat]:
    response = get_export_data(
        token,
        blaze_session,
        "TEAM_STATS",
        {"leagueId": LEAGUE_ID, "stageIndex": stage, "weekIndex": week_index},
    )
    if response.ok and response.json()["teamStatInfoList"]:
        data = response.json()
        try:
            return [
                MaddenTeamStat.model_validate(stat) for stat in data["teamStatInfoList"]
            ]
        except KeyError:
            raise Exception("STAT missing from teamStatInfoList!")
    else:
        raise Exception[
            f"Error getting Rushing Stats for Stage:{stage}, Week:{week_index}"
        ]


def get_free_agents(token: TokenInformation, session: BlazeSession, league_id: int):
    response = get_export_data(
        token,
        session,
        "TEAM_ROSTER",
        {"leagueId": LEAGUE_ID, "returnFreeAgents": True, "teamId": 0},
    )
    if response.ok:
        free_agents: list[MaddenPlayerData] = response.json()["rosterInfoList"]
        return free_agents
    else:
        raise Exception["Error getting Free Agents"]
