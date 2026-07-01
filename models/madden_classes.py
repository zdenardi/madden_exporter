from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

from pydantic.alias_generators import to_camel


class MaddenTeam(BaseModel):
    abbrName: str
    cityName: str
    defScheme: int
    displayName: str
    divName: str
    injuryCount: int
    logoId: int
    nickName: str
    offScheme: int
    ovrRating: int
    primaryColor: int
    secondaryColor: int
    teamId: int
    userName: str


class MaddenStandingsEntry(BaseModel):
    awayLosses: int
    awayTies: int
    calendarYear: int
    conferenceId: int
    confLosses: int
    conferenceName: str
    confTies: int
    confWins: int
    capRoom: int
    capAvailable: int
    capSpent: int
    defPassYds: int
    defPassYdsRank: int
    defRushYds: int
    defRushYdsRank: int
    defTotalYds: int
    defTotalYdsRank: int
    divisionId: int
    divLosses: int
    divisionName: str
    divTies: int
    divWins: int
    homeLosses: int
    homeTies: int
    homeWins: int
    netPts: int
    offPassYds: int
    offPassYdsRank: int
    offTotalYds: int
    offTotalYdsRank: int
    ptsAgainst: int
    ptsAgainstRank: int
    ptsFor: int
    rank: int
    seed: int
    seasonIndex: int
    stageIndex: int
    totalLosses: int
    totalTies: int
    totalWins: int
    teamId: int
    teamName: str
    teamOvr: int
    tODiff: int
    weekIndex: int
    winLossStreak: int
    winPct: float


class MaddenPlayerStatsBase(BaseModel):
    fullName: str
    rosterId: int  # ?
    scheduleId: int
    seasonIndex: int
    statId: int
    teamId: int
    weekIndex: int


class MaddenPlayerDefense(MaddenPlayerStatsBase):
    defCatchAllowed: int
    defDeflections: int
    defForcedFum: int
    defFumRec: int
    defInt: int
    defIntReturnYds: int
    defPts: int
    defSacks: int
    defSafeties: int
    defTDs: int
    defTotalTackles: int
    stageIndex: int


class MaddenPlayerKicking(MaddenPlayerStatsBase):
    kickPts: int
    fGatt: int
    fG50PlusAtt: int
    fG50PlusMade: int
    fGLongest: int
    fGMade: int
    fGCompPct: int
    kickoffAtt: int
    kickoffTBs: int
    xPAtt: int
    xPMade: int
    xPCompPct: int


class MaddenSignatureAbility(BaseModel):
    activationEnabled: bool = False
    deactivationEnabled: bool = False
    unlockRequirement: str = ""
    isUnlocked: bool = False
    marketplaceAbilityAlias: str = ""
    rank: str = "ABILITY_BRONZE"
    signatureActivationDescription: str = ""
    abilityGUID: str = ""
    activationId: str = ""
    signatureDeactivationDescription: str = ""
    deactivationId: str = ""
    isPassive: bool = False
    signatureDescription: str = ""
    signatureLogoId: int = 0
    signatureTitle: str = ""
    startActivated: bool = False


class MaddenRosterGoal(BaseModel):
    isEmpty: bool = True
    locked: bool = True
    ovrThreshold: Optional[int] = None
    signatureAbility: MaddenSignatureAbility = Field(
        default_factory=MaddenSignatureAbility
    )


class MaddenPlayerData(BaseModel):
    age: int = 0
    accelRating: int = 0
    isActive: bool = False
    agilityRating: int = 0
    awareRating: int = 0
    bCVRating: int = 0
    birthDay: Optional[int] = None
    bigHitTrait: int = 0
    blockShedRating: int = 0
    birthMonth: Optional[int] = None
    breakSackRating: int = 0
    breakTackleRating: int = 0
    birthYear: Optional[int] = None
    college: str = ""
    clutchTrait: int = 0
    confRating: int = 0
    capHit: int = 0
    capReleaseNetSavings: int = 0
    capReleasePenalty: int = 0
    contractBonus: int = 0
    carryRating: int = 0
    contractSalary: int = 0
    contractYearsLeft: Optional[int] = None
    contractLength: Optional[int] = None
    catchRating: int = 0
    cITRating: int = 0
    coverBallTrait: int = 0
    dLBullRushTrait: int = 0
    dLSpinTrait: int = 0
    dLSwimTrait: int = 0
    durabilityGrade: int = 0
    dropOpenPassTrait: int = 0
    draftPick: Optional[int] = None
    draftRound: Optional[int] = None
    desiredBonus: int = 0
    desiredSalary: int = 0
    desiredLength: Optional[int] = None
    devTrait: int = 0
    changeOfDirectionRating: int = 0
    fightForYardsTrait: int = 0
    firstName: str = ""
    finesseMovesRating: int = 0
    isFreeAgent: bool = False
    decisionMakerTrait: int = 0
    feetInBoundsTrait: int = 0
    height: Optional[int] = None
    highMotorTrait: int = 0
    hPCatchTrait: int = 0
    homeState: Optional[int] = None
    position: str = ""
    homeTown: str = ""
    hitPowerRating: int = 0
    impactBlockRating: int = 0
    isActive: bool = True
    injuryRating: int = 0
    injuryLength: Optional[int] = None
    isOnIR: bool = False
    intangibleGrade: int = 0
    injuryType: Optional[int] = None
    jukeMoveRating: int = 0
    jumpRating: int = 0
    jerseyNum: Optional[int] = None
    kickAccRating: int = 0
    kickPowerRating: int = 0
    kickRetRating: int = 0
    leadBlockRating: int = 0
    lBStyleTrait: int = 0
    legacyScore: int = 0
    lastName: str = ""
    manCoverRating: int = 0
    passBlockFinesseRating: int = 0
    passBlockPowerRating: int = 0
    playerBestOvr: Optional[int] = None
    physicalGrade: int = 0
    playActionRating: int = 0
    playBallTrait: int = 0
    playRecRating: int = 0
    longSnapRating: Optional[int] = None
    penaltyTrait: int = 0
    productionGrade: int = 0
    predictTrait: int = 0
    presentationId: Optional[int] = None
    isOnPracticeSquad: bool = False
    pressRating: int = 0
    pursuitRating: int = 0
    passBlockingRating: int = 0
    posCatchTrait: int = 0
    playerSchemeOvr: int = 0
    skillPoints: int = 0

    specCatchRating: int = 0
    speedRating: int = 0
    spinMoveRating: int = 0
    stripBallTrait: int = 0
    stiffArmRating: Optional[int] = None
    staminaRating: int = 0
    strengthRating: int = 0
    tackleRating: int = 0
    toughRating: int = 0
    tightSpiralTrait: int = 0
    throwAccRating: int = 0
    throwAccDeepRating: Optional[int] = None
    throwAccMidRating: Optional[int] = None
    throwAccShortRating: Optional[int] = None
    throwAwayTrait: int = 0
    throwPowerRating: int = 0
    throwOnRunRating: int = 0
    throwUnderPressureRating: int = 0
    teamId: Optional[int] = None
    truckRating: int = 0
    teamSchemeOvr: Optional[int] = None
    weight: Optional[int] = None
    experiencePoints: int = 0
    yACCatchTrait: int = 0
    yearsPro: Optional[int] = None
    zoneCoverRating: int = 0
    rosterId: int

    rosterGoalList: List[Optional[MaddenRosterGoal]] = Field(default_factory=list)  # type: ignore


class MaddenScheduleEntry(BaseModel):
    awayScore: int
    awayTeamId: int
    isGameOfTheWeek: bool
    homeScore: int
    homeTeamId: int
    scheduleId: int
    seasonIndex: int
    stageIndex: int
    status: int
    weekIndex: int


class MaddenBaseStat(BaseModel):
    fullName: str
    rosterId: int
    scheduleId: int
    seasonIndex: int
    statId: int
    stageIndex: int
    teamId: int
    weekIndex: int


class MaddenPassingStat(MaddenBaseStat):
    passAtt: int
    passComp: int
    passCompPct: float
    passInts: int
    passLongest: int
    passPts: int
    passerRating: float
    passSacks: int
    passTDs: int
    passYds: int
    passYdsPerAtt: float
    passYdsPerGame: float


class MaddenReceivingStat(MaddenBaseStat):
    recCatches: int
    recCatchPct: float
    recDrops: int
    recLongest: int
    recPts: int
    recTDs: int
    recToPct: float
    recYdsAfterCatch: int
    recYacPerCatch: float
    recYds: int
    recYdsPerCatch: float
    recYdsPerGame: float


class MaddenRushingStat(MaddenBaseStat):
    rushAtt: int
    rushBrokenTackles: int
    rushFum: int
    rushLongest: int
    rushToPct: float
    rushTDs: int
    rush20PlusYds: int
    rushYdsAfterContact: int
    rushYds: int
    rushYdsPerAtt: float
    rushYdsPerGame: float


class MaddenDefensiveStat(MaddenBaseStat):
    defCatchAllowed: int
    defDeflections: int
    defForcedFum: int
    defFumRec: int
    defInts: int
    defIntReturnYds: int
    defPts: int
    defSacks: int
    defSafeties: int
    defTDs: int
    defTotalTackles: int


class MaddenPuntingStat(MaddenBaseStat):
    puntsBlocked: int
    puntsIn20: int
    puntLongest: int
    puntTBs: int
    puntNetYdsPerAtt: float
    puntNetYds: int
    puntAtt: int
    puntYdsPerAtt: float
    puntYds: int


class MaddenKickingStat(MaddenBaseStat):
    kickPts: int
    fGAtt: int
    fG50PlusAtt: int
    fG50PlusMade: int
    fGLongest: int
    fGMade: int
    fGCompPct: float
    kickoffAtt: int
    kickoffTBs: int

    xPAtt: int
    xPMade: int
    xPCompPct: float


class MaddenGameStat(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    def_forced_fum: int
    def_fum_rec: int
    def_ints_rec: int
    def_pts_per_game: float
    def_pass_yds: int
    def_rush_yds: int
    def_red_zone_fgs: int
    def_red_zones: int
    def_red_zone_pct: float
    def_red_zone_tds: int
    def_sacks: int
    def_total_yds: int

    off_4th_down_att: int
    off_4th_down_conv: int
    off_4th_down_conv_pct: float

    off_fum_lost: int
    off_ints_lost: int

    off_1st_downs: int
    off_pts_per_game: float

    off_pass_tds: int
    off_pass_yds: int

    off_rush_tds: int
    off_rush_yds: int

    off_red_zone_fgs: int
    off_red_zones: int
    off_red_zone_pct: float
    off_red_zone_tds: int

    off_sacks: int

    off_3rd_down_att: int
    off_3rd_down_conv: int
    off_3rd_down_conv_pct: float

    off_2pt_att: int
    off_2pt_conv: int
    off_2pt_conv_pct: float

    off_total_yds: int
    off_total_yds_gained: int

    penalties: int
    penalty_yds: int

    schedule_id: int
    seed: int
    season_index: int
    stat_id: int
    stage_index: int

    total_losses: int
    team_id: int

    to_diff: int
    to_giveaways: int
    to_takeaways: int

    total_ties: int
    total_wins: int

    week_index: int
