from typing import Literal

LEAGUE_ID = 27435432
AUTH_SOURCE = 317239
CLIENT_SECRET = (
    "teJpJ9cSXFqZAuKNW8IuHpy8D4dwWPoVrPoek38iCnrGbrUSfjqnHMBAv8iCVjeSm_20250910175618"
)
REDIRECT_URL = "http://127.0.0.1/success"
CLIENT_ID = "MCA_26_COMP_APP"
MACHINE_KEY = "444d362e8e067fe2"
EA_LOGIN_URL = f"https://accounts.ea.com/connect/auth?hide_create=true&release_type=prod&response_type=code&redirect_uri={REDIRECT_URL}&client_id={CLIENT_ID}&machineProfileKey={MACHINE_KEY}&authentication_source={AUTH_SOURCE}"

LeagueData = {
    "TEAMS": "CareerMode_GetLeagueTeamsExport",
    "STANDINGS": "CareerMode_GetStandingsExport",
    "WEEKLY_SCHEDULE": "CareerMode_GetWeeklySchedulesExport",
    "RUSHING_STATS": "CareerMode_GetWeeklyRushingStatsExport",
    "TEAM_STATS": "CareerMode_GetWeeklyTeamStatsExport",
    "PUNTING_STATS": "CareerMode_GetWeeklyPuntingStatsExport",
    "RECEIVING_STATS": "CareerMode_GetWeeklyReceivingStatsExport",
    "DEFENSIVE_STATS": "CareerMode_GetWeeklyDefensiveStatsExport",
    "KICKING_STATS": "CareerMode_GetWeeklyKickingStatsExport",
    "PASSING_STATS": "CareerMode_GetWeeklyPassingStatsExport",
    "TEAM_ROSTER": "CareerMode_GetTeamRostersExport",
}
LeagueDataKey = Literal[
    "TEAMS",
    "STANDINGS",
    "WEEKLY_SCHEDULE",
    "RUSHING_STATS",
    "TEAM_STATS",
    "PUNTING_STATS",
    "RECEIVING_STATS",
    "DEFENSIVE_STATS",
    "KICKING_STATS",
    "PASSING_STATS",
    "TEAM_ROSTER",
]
