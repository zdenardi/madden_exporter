# Gets from Standings Resource
from sqlalchemy.orm import Session
from sqlalchemy import select

from db import (
    DefensiveStat,
    Game,
    KickingStat,
    PassingStat,
    PuntingStat,
    ReceivingStat,
    RushingStat,
    TeamStats,
)
from madden_classes import (
    MaddenDefensiveStat,
    MaddenKickingStat,
    MaddenPassingStat,
    MaddenPuntingStat,
    MaddenReceivingStat,
    MaddenRushingStat,
    MaddenStandingsEntry,
)


def upsert_stat(session: Session, entry: MaddenStandingsEntry):
    stmt = select(TeamStats).where(
        TeamStats.team_id == entry.teamId, TeamStats.season == entry.seasonIndex
    )
    existing = session.execute(stmt).scalars().first()

    if existing:
        existing.wins = entry.totalWins
        existing.losses = entry.totalLosses
        existing.week = entry.weekIndex
        existing.points_for = entry.ptsFor
        existing.points_against = entry.ptsAgainst
        existing.standings_rank = entry.rank
        existing.yards = entry.offTotalYds
        existing.turnovers = entry.tODiff
        return existing
    else:
        team_stat = TeamStats(
            team_id=entry.teamId,
            season=entry.seasonIndex,
            week=entry.weekIndex,
            wins=entry.totalWins,
            losses=entry.totalLosses,
            points_for=entry.ptsFor,
            points_against=entry.ptsAgainst,
            standings_rank=entry.rank,
            yards=entry.offTotalYds,
            turnovers=entry.tODiff,
        )
        session.add(team_stat)
        return team_stat


def upsert_pass(session: Session, stat: MaddenPassingStat):
    stmt = select(PassingStat).where(
        PassingStat.roster_id == stat.rosterId,
        PassingStat.season == stat.seasonIndex,
        PassingStat.week == stat.weekIndex,
    )
    existing = session.execute(stmt).scalar_one_or_none()
    if existing:
        # Upsert
        existing.pass_att = stat.passAtt
        existing.pass_comp = stat.passComp
        existing.pass_comp_pct = stat.passCompPct
        existing.pass_int = stat.passInts
        existing.pass_longest = stat.passLongest
        existing.pass_pts = stat.passPts
        existing.passer_rating = stat.passerRating
        existing.pass_sacks = stat.passSacks
        existing.pass_tds = stat.passTDs
        existing.pass_yds = stat.passYds
        existing.pass_yds_per_att = stat.passYdsPerAtt
        existing.pass_yds_per_game = stat.passYdsPerGame
        return existing
    else:
        game = session.scalar(select(Game).where(Game.schedule_id == stat.scheduleId))

        if game is None:
            raise ValueError(
                f"Game {stat.scheduleId} not found, can not add passing stat!"
            )

        passing = PassingStat(
            game=game,
            roster_id=stat.rosterId,
            season=stat.seasonIndex,
            stage=stat.stageIndex,
            team_id=stat.teamId,
            week=stat.weekIndex,
            pass_att=stat.passAtt,
            pass_comp=stat.passComp,
            pass_comp_pct=stat.passCompPct,
            pass_ints=stat.passInts,
            pass_longest=stat.passLongest,
            pass_pts=stat.passPts,
            passer_rating=stat.passerRating,
            pass_sacks=stat.passSacks,
            pass_tds=stat.passTDs,
            pass_yds=stat.passYds,
            pass_yds_per_att=stat.passYdsPerAtt,
            pass_yds_per_game=stat.passYdsPerGame,
        )

        session.add(passing)
        return passing


def upsert_rush(session: Session, stat: MaddenRushingStat):
    stmt = select(RushingStat).where(
        RushingStat.roster_id == stat.rosterId,
        RushingStat.season == stat.seasonIndex,
        RushingStat.week == stat.weekIndex,
    )
    existing = session.execute(stmt).scalar_one_or_none()

    if existing:
        existing.rush_att = stat.rushAtt
        existing.rush_longest = stat.rushLongest
        existing.rush_broken_tackles = stat.rushBrokenTackles
        existing.rush_fum = stat.rushFum
        existing.rush_to_pct = stat.rushToPct
        existing.rush_tds = stat.rushTDs
        existing.rush_20_plus_yards = stat.rush20PlusYds
        existing.rush_yds_after_contact = stat.rushYdsAfterContact
        existing.rush_yds = stat.rushYds
        existing.rush_yds_per_att = stat.rushYdsPerAtt
        existing.rush_yds_per_game = stat.rushYdsPerGame
        return existing
    else:
        game = session.scalar(select(Game).where(Game.schedule_id == stat.scheduleId))

        if game is None:
            raise ValueError(
                f"Game {stat.scheduleId} not found, could not add Rushing Stat"
            )

        rush = RushingStat(
            game=game,
            game_id=game.id,
            roster_id=stat.rosterId,
            season=stat.seasonIndex,
            stage=stat.stageIndex,
            team_id=stat.teamId,
            week=stat.weekIndex,
            rush_att=stat.rushAtt,
            rush_broken_tackles=stat.rushBrokenTackles,
            rush_fum=stat.rushFum,
            rush_to_pct=stat.rushToPct,
            rush_tds=stat.rushTDs,
            rush_20_plus_yards=stat.rush20PlusYds,
            rush_yds_after_contact=stat.rushYdsAfterContact,
            rush_yds=stat.rushYds,
            rush_yds_per_att=stat.rushYdsPerAtt,
            rush_yds_per_game=stat.rushYdsPerGame,
            rush_longest=stat.rushLongest,
        )
        session.add(rush)
        return rush


def upsert_rec(session: Session, stat: MaddenReceivingStat):
    stmt = select(ReceivingStat).where(
        ReceivingStat.roster_id == stat.rosterId,
        ReceivingStat.season == stat.seasonIndex,
        ReceivingStat.week == stat.weekIndex,
    )
    existing = session.execute(stmt).scalar_one_or_none()

    if existing:
        existing.rec_catches = stat.recCatches
        existing.rec_catch_pct = stat.recCatchPct
        existing.rec_drops = stat.recDrops
        existing.rec_longest = stat.recLongest
        existing.rec_pts = stat.recPts
        existing.rec_tds = stat.recTDs
        existing.rec_to_pct = stat.recToPct
        existing.rec_yds_after_catch = stat.recYdsAfterCatch
        existing.rec_yac_per_catch = stat.recYacPerCatch
        existing.rec_yds = stat.recYds
        existing.rec_yds_per_catch = stat.recYdsPerCatch
        existing.rec_yds_per_game = stat.recYdsPerGame
        return existing
    else:
        game = session.scalar(select(Game).where(Game.schedule_id == stat.scheduleId))

        if game is None:
            raise ValueError(
                f"Game {stat.scheduleId} not found, cannot create Receiving Stat!"
            )

        rec = ReceivingStat(
            game=game,
            game_id=game.id,
            roster_id=stat.rosterId,
            season=stat.seasonIndex,
            stage=stat.stageIndex,
            team_id=stat.teamId,
            week=stat.weekIndex,
            rec_catches=stat.recCatches,
            rec_catch_pct=stat.recCatchPct,
            rec_drops=stat.recDrops,
            rec_longest=stat.recLongest,
            rec_pts=stat.recPts,
            rec_tds=stat.recTDs,
            rec_to_pct=stat.recToPct,
            rec_yds_after_catch=stat.recYdsAfterCatch,
            rec_yac_per_catch=stat.recYacPerCatch,
            rec_yds=stat.recYds,
            rec_yds_per_catch=stat.recYdsPerCatch,
            rec_yds_per_game=stat.recYdsPerGame,
        )
        session.add(rec)
        return rec


def upsert_def(session, stat: MaddenDefensiveStat):
    stmt = select(DefensiveStat).where(
        DefensiveStat.roster_id == stat.rosterId,
        DefensiveStat.season == stat.seasonIndex,
        DefensiveStat.week == stat.weekIndex,
    )
    existing = session.execute(stmt).scalar_one_or_none()

    if existing:
        existing.def_catch_allowed = stat.defCatchAllowed
        existing.def_deflections = stat.defDeflections
        existing.def_forced_fumble = stat.defForcedFum
        existing.def_fum_rec = stat.defFumRec
        existing.def_ints = stat.defInts
        existing.def_int_return_yds = stat.defIntReturnYds
        existing.def_pts = stat.defPts
        existing.def_sacks = stat.defSacks
        existing.def_safeties = stat.defSafeties
        existing.def_tds = stat.defTDs
        existing.def_total_tackles = stat.defTotalTackles
        return existing
    else:
        game = session.scalar(select(Game).where(Game.schedule_id == stat.scheduleId))
        if game is None:
            raise ValueError(
                f"Game {stat.scheduleId} not found, could not add Defensive stat"
            )
        def_stat = DefensiveStat(
            game=game,
            game_id=game.id,
            roster_id=stat.rosterId,
            season=stat.seasonIndex,
            stage=stat.stageIndex,
            team_id=stat.teamId,
            week=stat.weekIndex,
            def_catch_allowed=stat.defCatchAllowed,
            def_deflections=stat.defDeflections,
            def_forced_fum=stat.defForcedFum,
            def_fum_rec=stat.defFumRec,
            def_ints=stat.defInts,
            def_int_return_yds=stat.defIntReturnYds,
            def_pts=stat.defPts,
            def_sacks=stat.defSacks,
            def_safeties=stat.defSafeties,
            def_tds=stat.defTDs,
            def_total_tackles=stat.defTotalTackles,
        )
        session.add(def_stat)
        return def_stat


def upsert_punt(session, stat: MaddenPuntingStat):
    stmt = select(PuntingStat).where(
        PuntingStat.roster_id == stat.rosterId,
        PuntingStat.season == stat.seasonIndex,
        PuntingStat.week == stat.weekIndex,
    )
    existing: PuntingStat = session.execute(stmt).scalar_one_or_none()

    if existing:
        existing.punt_blocked = stat.puntsBlocked
        existing.punts_in_20 = stat.puntsIn20
        existing.punt_longest = stat.puntLongest
        existing.punt_tbs = stat.puntTBs
        existing.punt_net_yds_per_att = stat.puntNetYdsPerAtt
        existing.punt_net_yds = stat.puntNetYds
        existing.punt_att = stat.puntAtt
        existing.punt_yds_per_att = stat.puntYdsPerAtt
        existing.punt_yds = stat.puntYds
        return existing
    else:
        game = session.scalar(select(Game).where(Game.schedule_id == stat.scheduleId))
        if game is None:
            raise ValueError(
                f"Game {stat.scheduleId} not found, could not add Punting Stat"
            )
        punting_stat = PuntingStat(
            game=game,
            game_id=game.id,
            roster_id=stat.rosterId,
            season=stat.seasonIndex,
            stage=stat.stageIndex,
            team_id=stat.teamId,
            week=stat.weekIndex,
            punt_blocked=stat.puntsBlocked,
            punts_in_20=stat.puntsIn20,
            punt_longest=stat.puntLongest,
            punt_tbs=stat.puntTBs,
            punt_net_yds_per_att=stat.puntNetYdsPerAtt,
            punt_net_yds=stat.puntNetYds,
            punt_att=stat.puntAtt,
            punt_yds_per_att=stat.puntYdsPerAtt,
            punt_yds=stat.puntYds,
        )
        session.add(punting_stat)
        return punting_stat


def upsert_kick(session, stat: MaddenKickingStat):
    stmt = select(KickingStat).where(
        KickingStat.roster_id == stat.rosterId,
        KickingStat.season == stat.seasonIndex,
        KickingStat.week == stat.weekIndex,
    )
    existing = session.execute(stmt).scalar_one_or_none()

    if existing:
        existing.kick_pts = stat.kickPts
        existing.fg_att = stat.fGAtt
        existing.fg_50_plus_att = stat.fG50PlusAtt
        existing.fg_50_plus_made = stat.fG50PlusMade
        existing.fg_longest = stat.fGLongest
        existing.fg_made = stat.fGMade
        existing.fg_comp_pct = stat.fGCompPct
        existing.kick_off_att = stat.kickoffAtt
        existing.kick_off_tbs = stat.kickoffTBs
        existing.xp_att = stat.xPAtt
        existing.xp_made = stat.xPMade
        existing.xp_comp_pct = stat.xPCompPct
        return existing
    else:
        game = session.scalar(select(Game).where(Game.schedule_id == stat.scheduleId))
        if game is None:
            raise ValueError(
                f"Game {stat.scheduleId} not found, could not add kicking stat"
            )
        kicking_stat = KickingStat(
            game=game,
            game_id=game.id,
            roster_id=stat.rosterId,
            season=stat.seasonIndex,
            stage=stat.stageIndex,
            team_id=stat.teamId,
            week=stat.weekIndex,
            kick_pts=stat.kickPts,
            fg_att=stat.fGAtt,
            fg_50_plus_att=stat.fG50PlusAtt,
            fg_50_plus_made=stat.fG50PlusMade,
            fg_longest=stat.fGLongest,
            fg_made=stat.fGMade,
            fg_comp_pct=stat.fGCompPct,
            kick_off_att=stat.kickoffAtt,
            kick_off_tbs=stat.kickoffTBs,
            xp_att=stat.xPAtt,
            xp_made=stat.xPMade,
            xp_comp_pct=stat.xPCompPct,
        )
        session.add(kicking_stat)
        return kicking_stat
