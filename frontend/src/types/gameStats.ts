import { PlayerStatBase, PlayerResponse } from './player';

/**
 * PassingStats models the passing statistics for a player.
 * Extends PlayerStatBase.
 */
export interface PassingStats extends PlayerStatBase {
    passAtt: number;
    passComp: number;
    passCompPct: number;
    passInts: number;
    passLongest: number;
    passPts: number;
    passerRating: number;
    passSacks: number;
    passTds: number;
    passYds: number;
    passYdsPerAtt: number;
    passYdsPerGame: number;
}

/**
 * RushingStats models the rushing statistics for a player.
 * Extends PlayerStatBase.
 */
export interface RushingStats extends PlayerStatBase {
    rushAtt: number;
    rushBrokenTackles: number;
    rushFum: number;
    rushLongest: number;
    rushToPct: number;
    rushTds: number;
    rush20PlusYards: number;
    rushYdsAfterContact: number;
    rushYds: number;
    rushYdsPerAtt: number;
    rushYdsPerGame: number;
}

/**
 * ReceivingStats models the receiving statistics for a player.
 * Extends PlayerStatBase.
 */
export interface ReceivingStats extends PlayerStatBase {
    recCatches: number;
    recCatchPct: number;
    recDrops: number;
    recLongest: number;
    recPts: number;
    recTds: number;
    recToPct: number;
    recYadPerCatch: number;
    recYds: number;
    recYdsPerCatch: number;
    recYdsPerGame: number;
}

/**
 * DefenseStats models defensive statistics for a player.
 * Extends PlayerStatBase.
 */
export interface DefenseStats extends PlayerStatBase {
    defCatchAllowed: number;
    defDeflections: number;
    defForcedFum: number;
    defFumRec: number;
    defInts: number;
    defIntReturnYds: number;
    defPts: number;
    defSacks: number;
    defSafeties: number;
    defTds: number;
    defTotalTackles: number;
}

/**
 * KickingStats models the kicking statistics for a player.
 * Extends PlayerStatBase.
 */
export interface KickingStats extends PlayerStatBase {
    kickPts: number;
    fgAtt: number;
    fg50PlusAtt: number;
    fg50PlusMade: number;
    fgLongest: number;
    fgMade: number;
    fgCompPct: number;
    kickOffAtt: number;
    kickOffTbs: number;
    xpAtt: number;
    xpMade: number;
    xpCompPct: number;
}

/**
 * PuntingStats models the punting statistics for a player.
 * Extends PlayerStatBase.
 */
export interface PuntingStats extends PlayerStatBase {
    puntBlocked: number;
    puntsIn20: number;
    puntLongest: number;
    puntTbs: number;
    puntNetYdsPerAtt: number;
    puntNetYds: number;
    puntAtt: number;
    puntYdsPerAtt: number;
    puntYds: number;
}