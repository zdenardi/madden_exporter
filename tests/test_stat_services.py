from db import Game, PassingStat, Player
from madden_classes import (
    MaddenDefensiveStat,
    MaddenKickingStat,
    MaddenPassingStat,
    MaddenPuntingStat,
    MaddenReceivingStat,
    MaddenRushingStat,
)
from services.stat_services import (
    upsert_def,
    upsert_kick,
    upsert_pass,
    upsert_punt,
    upsert_rec,
    upsert_rush,
)


def test_upsert_passing_create(session, player: Player, game: Game):

    assert session.query(PassingStat).count() == 0
    madden_passing = MaddenPassingStat(
        fullName=player.first_name + " " + player.last_name,
        rosterId=player.roster_id,
        scheduleId=game.schedule_id,
        seasonIndex=game.season_index,
        statId=1,
        stageIndex=0,
        teamId=player.team_id,
        weekIndex=game.week_index,
        passAtt=20,
        passComp=18,
        passCompPct=18 / 20,
        passInt=1,
        passLongest=25,
        passPts=0,
        passerRating=101.1,
        passSacks=1,
        passTds=2,
        passYds=300,
        passYdsPerAtt=300 / 18,
        passYdsPerGame=300,
    )

    stat = upsert_pass(session, madden_passing)
    session.flush()
    assert stat is not None
    assert stat.game == game


def test_upsert_passing_upsert(
    session, passing_stat: PassingStat, team_1, game, player
):
    assert passing_stat.pass_int == 0
    madden_passing = MaddenPassingStat(
        fullName="J. Doe",
        rosterId=passing_stat.roster_id,
        scheduleId=game.schedule_id,
        seasonIndex=passing_stat.season,
        statId=1,
        stageIndex=0,
        teamId=player.team_id,
        weekIndex=passing_stat.week,
        passAtt=20,
        passComp=18,
        passCompPct=18 / 20,
        passInt=1,
        passLongest=25,
        passPts=0,
        passerRating=101.1,
        passSacks=1,
        passTds=2,
        passYds=300,
        passYdsPerAtt=300 / 18,
        passYdsPerGame=300,
    )

    stat = upsert_pass(session, madden_passing)
    session.flush()
    assert stat.id == passing_stat.id
    assert stat.pass_int == 1


def test_upsert_rushing_create(session, player, game):

    stat_dict = {
        "fullName": "A.Leno",
        "rushAtt": 7,
        "rushBrokenTackles": 1,
        "rushFum": 0,
        "rushLongest": 6,
        "rushPts": 0,
        "rosterId": player.roster_id,
        "rushTDs": 1,
        "rushToPct": 0.0,
        "rush20PlusYds": 0,
        "rushYdsAfterContact": 1,
        "rushYds": 23,
        "rushYdsPerAtt": 3.28571,
        "rushYdsPerGame": 19.4,
        "scheduleId": game.schedule_id,
        "seasonIndex": 12,
        "statId": 538055444,
        "stageIndex": 1,
        "teamId": game.away_team_id,
        "weekIndex": game.week_index,
    }

    madden_rushing = MaddenRushingStat.model_validate(stat_dict)
    stat = upsert_rush(session, madden_rushing)
    assert stat.game_id == game.id
    assert stat.rush_yds == 23


def test_upsert_rushing_upsert(session, player, game, rushing_stat):

    stat_dict = {
        "fullName": "N.Name",
        "rushAtt": 7,
        "rushBrokenTackles": 3,
        "rushFum": 0,
        "rushLongest": 6,
        "rushPts": 0,
        "rosterId": rushing_stat.roster_id,
        "rushTDs": 3,
        "rushToPct": 0.0,
        "rush20PlusYds": 0,
        "rushYdsAfterContact": 1,
        "rushYds": 100,
        "rushYdsPerAtt": 3.28571,
        "rushYdsPerGame": 19.4,
        "scheduleId": game.schedule_id,
        "seasonIndex": rushing_stat.season,
        "statId": 538055444,
        "stageIndex": 1,
        "teamId": game.away_team_id,
        "weekIndex": rushing_stat.week,
    }

    madden_rushing = MaddenRushingStat.model_validate(stat_dict)
    stat = upsert_rush(session, madden_rushing)
    assert stat.id == rushing_stat.id
    assert stat.game_id == game.id
    assert stat.rush_yds == 100
    assert stat.rush_tds == 3


def test_upsert_def_create(session, player, game):
    def_dict = {
        "defCatchAllowed": 0,
        "defDeflections": 1,
        "defForcedFum": 0,
        "defFumRec": 0,
        "defInts": 0,
        "defIntReturnYds": 0,
        "defPts": 0,
        "defSacks": 1.0,
        "defSafeties": 0,
        "defTDs": 0,
        "defTotalTackles": 1,
        "fullName": "L.Washington",
        "rosterId": player.roster_id,
        "scheduleId": game.schedule_id,
        "seasonIndex": 1,
        "statId": 545664268,
        "stageIndex": 1,
        "teamId": 775553055,
        "weekIndex": game.week_index,
    }
    madden_def_stat = MaddenDefensiveStat.model_validate(def_dict)
    stat = upsert_def(session, madden_def_stat)
    assert stat.game == game
    assert stat.def_total_tackles == 1


def test_upsert_def_upsert(session, player, game, def_stat):
    def_dict = {
        "defCatchAllowed": 0,
        "defDeflections": 1,
        "defForcedFum": 0,
        "defFumRec": 0,
        "defInts": 0,
        "defIntReturnYds": 500,
        "defPts": 0,
        "defSacks": 1.0,
        "defSafeties": 0,
        "defTDs": 0,
        "defTotalTackles": 1,
        "fullName": "L.Washington",
        "rosterId": player.roster_id,
        "scheduleId": game.schedule_id,
        "seasonIndex": game.season_index,
        "statId": 545664268,
        "stageIndex": 1,
        "teamId": 775553055,
        "weekIndex": game.week_index,
    }
    madden_def_stat = MaddenDefensiveStat.model_validate(def_dict)
    stat = upsert_def(session, madden_def_stat)
    assert stat.def_int_return_yds == 500


def test_upsert_punting_create(session, player, game):
    punt_dict = {
        "fullName": "C.Gold",
        "puntsBlocked": 0,
        "puntsIn20": 0,
        "puntLongest": 43,
        "puntTBs": 0,
        "puntNetYdsPerAtt": 25.0,
        "puntNetYds": 25,
        "puntAtt": 1,
        "puntYdsPerAtt": 43.0,
        "puntYds": 43,
        "rosterId": player.roster_id,
        "scheduleId": 1,
        "seasonIndex": 1,
        "statId": 547618970,
        "stageIndex": 1,
        "teamId": game.away_team_id,
        "weekIndex": 1,
    }
    madden_punt_stat = MaddenPuntingStat.model_validate(punt_dict)
    stat = upsert_punt(session, madden_punt_stat)
    stat.game == game


def test_upsert_punting_edit(session, player, game, punting_stat):
    punt_dict = {
        "fullName": "C.Gold",
        "puntsBlocked": 0,
        "puntsIn20": 1,
        "puntLongest": 43,
        "puntTBs": 1,
        "puntNetYdsPerAtt": 25.0,
        "puntNetYds": 25,
        "puntAtt": 1,
        "puntYdsPerAtt": 43.0,
        "puntYds": 43,
        "rosterId": player.roster_id,
        "seasonIndex": punting_stat.season,
        "stageIndex": 1,
        "statId": 1,
        "scheduleId": game.schedule_id,
        "teamId": game.away_team_id,
        "weekIndex": punting_stat.week,
    }
    madden_punt_stat = MaddenPuntingStat.model_validate(punt_dict)
    stat = upsert_punt(session, madden_punt_stat)
    stat.game == game
    stat.punt_yds_per_att = 43


def test_upsert_kicking_create(session, player, game):
    dict = {
        "kickPts": 0,
        "fGAtt": 0,
        "fG50PlusAtt": 0,
        "fG50PlusMade": 0,
        "fGLongest": 0,
        "fGMade": 0,
        "fGCompPct": 0.0,
        "fullName": "C.Gold",
        "kickoffAtt": 5,
        "kickoffTBs": 2,
        "rosterId": player.roster_id,
        "scheduleId": game.schedule_id,
        "seasonIndex": 1,
        "statId": 547618970,
        "stageIndex": 1,
        "teamId": game.away_team_id,
        "weekIndex": 1,
        "xPAtt": 0,
        "xPMade": 0,
        "xPCompPct": 0.0,
    }
    madden_kick_stat = MaddenKickingStat.model_validate(dict)
    stat = upsert_kick(session, madden_kick_stat)
    stat.game == game


def test_upsert_kicking_edit(session, player, game, kicking_stat):
    dict = {
        "kickPts": 0,
        "fGAtt": 0,
        "fG50PlusAtt": 0,
        "fG50PlusMade": 0,
        "fGLongest": 75,
        "fGMade": 0,
        "fGCompPct": 0.0,
        "fullName": "C.Gold",
        "kickoffAtt": 5,
        "kickoffTBs": 2,
        "rosterId": player.roster_id,
        "scheduleId": game.schedule_id,
        "seasonIndex": game.schedule_id,
        "statId": 547618970,
        "stageIndex": 1,
        "teamId": player.team_id,
        "weekIndex": game.week_index,
        "xPAtt": 0,
        "xPMade": 0,
        "xPCompPct": 0.0,
    }
    madden_kick_stat = MaddenKickingStat.model_validate(dict)
    stat = upsert_kick(session, madden_kick_stat)
    stat.game == game
    stat.fg_longest = 75


def test_upsert_rec_create(session, player, game):
    dict = {
        "fullName": "J. Doe",
        "recCatches": 3,
        "recCatchPct": 100.0,
        "recDrops": 0,
        "recLongest": 20,
        "recPts": 0,
        "rosterId": 553386878,
        "recTDs": 0,
        "recToPct": 0.0,
        "recYdsAfterCatch": 18,
        "recYacPerCatch": 6.0,
        "recYds": 29,
        "recYdsPerCatch": 9.66667,
        "recYdsPerGame": 36.0,
        "scheduleId": game.schedule_id,
        "seasonIndex": 1,
        "statId": 538056571,
        "stageIndex": 1,
        "teamId": player.team_id,
        "weekIndex": 1,
    }
    madden_rec_stat = MaddenReceivingStat.model_validate(dict)
    stat = upsert_rec(session, madden_rec_stat)
    stat.game == game


def test_upsert_rec_edit(session, player, game, rec_stat):
    dict = {
        "fullName": "J. Doe",
        "recCatches": 5,
        "recCatchPct": 100.0,
        "recDrops": 0,
        "recLongest": 75,
        "recPts": 0,
        "rosterId": 553386878,
        "recTDs": 0,
        "recToPct": 0.0,
        "recYdsAfterCatch": 18,
        "recYacPerCatch": 6.0,
        "recYds": 29,
        "recYdsPerCatch": 9.66667,
        "recYdsPerGame": 36.0,
        "scheduleId": game.schedule_id,
        "seasonIndex": game.season_index,
        "statId": 538056571,
        "stageIndex": 1,
        "teamId": player.team_id,
        "weekIndex": game.week_index,
    }
    madden_rec_stat = MaddenReceivingStat.model_validate(dict)
    stat = upsert_rec(session, madden_rec_stat)
    stat.game == game
    stat.recLongest = 75
