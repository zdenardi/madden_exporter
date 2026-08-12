from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from data_classes.data_classes import HumanGameSummary
from models import TeamGameSummary
from models.game import Game


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


class MaddenTeamStat(BaseModel):
    defForcedFum: int
    defFumRec: int
    defIntsRec: int
    defPtsPerGame: float
    defPassYds: int
    defRushYds: int
    defRedZoneFGs: int
    defRedZones: int
    defRedZonePct: float
    defRedZoneTDs: int
    defSacks: int
    defTotalYds: int
    off4thDownAtt: int
    off4thDownConv: int
    off4thDownConvPct: float
    offFumLost: int
    offIntsLost: int
    off1stDowns: int
    offPtsPerGame: float
    offPassTDs: int
    offPassYds: int
    offRushTDs: int
    offRushYds: int
    offRedZoneFGs: int
    offRedZones: int
    offRedZonePct: float
    offRedZoneTDs: int
    offSacks: int
    off3rdDownAtt: int
    off3rdDownConv: int
    off3rdDownConvPct: float
    off2PtAtt: int
    off2PtConv: int
    off2PtConvPct: float
    offTotalYds: int
    offTotalYdsGained: int
    penalties: int
    penaltyYds: int
    scheduleId: float
    seed: int
    seasonIndex: int
    statId: int
    stageIndex: int
    totalLosses: int
    teamId: int
    tODiff: int
    tOGiveaways: int
    tOTakeaways: int
    totalTies: int
    totalWins: int
    weekIndex: int

    def to_db_model(self, game: Game) -> TeamGameSummary:
        return TeamGameSummary(
            team_id=self.teamId,
            stat_id=self.statId,
            game_id=game.id,
            schedule_id=self.scheduleId,
            week_index=self.weekIndex,
            def_forced_fum=self.defForcedFum,
            def_fum_rec=self.defFumRec,
            def_ints_rec=self.defIntsRec,
            def_pts_per_game=self.defPtsPerGame,
            def_pass_yds=self.defPassYds,
            def_rush_yds=self.defRushYds,
            def_red_zone_fgs=self.defRedZoneFGs,
            def_red_zones=self.defRedZones,
            def_red_zone_pct=self.defRedZonePct,
            def_red_zone_tds=self.defRedZoneTDs,
            def_sacks=self.defSacks,
            def_total_yds=self.defTotalYds,
            off_4th_down_att=self.off4thDownAtt,
            off_4th_down_conv=self.off4thDownConv,
            off_4th_down_conv_pct=self.off4thDownConvPct,
            off_fum_lost=self.offFumLost,
            off_ints_lost=self.offIntsLost,
            off_1st_downs=self.off1stDowns,
            off_pts_per_game=self.offPtsPerGame,
            off_pass_tds=self.offPassTDs,
            off_pass_yds=self.offPassYds,
            off_rush_tds=self.offRushTDs,
            off_rush_yds=self.offRushYds,
            off_red_zone_fgs=self.offRedZoneFGs,
            off_red_zones=self.offRedZones,
            off_red_zone_pct=self.offRedZonePct,
            off_red_zone_tds=self.offRedZoneTDs,
            off_sacks=self.offSacks,
            off_3rd_down_att=self.off3rdDownAtt,
            off_3rd_down_conv=self.off3rdDownConv,
            off_3rd_down_conv_pct=self.off3rdDownConvPct,
            off_2pt_att=self.off2PtAtt,
            off_2pt_conv=self.off2PtConv,
            off_2pt_conv_pct=self.off2PtConvPct,
            off_total_yds=self.offTotalYds,
            off_total_yds_gained=self.offTotalYdsGained,
            penalties=self.penalties,
            penalty_yds=self.penaltyYds,
            seed=self.seed,
            season_index=self.seasonIndex,
            stage_index=self.stageIndex,
            total_losses=self.totalLosses,
            total_ties=self.totalTies,
            total_wins=self.totalWins,
            to_diff=self.tODiff,
            to_giveaways=self.tOGiveaways,
            to_takeaways=self.tOTakeaways,
        )

    def update_from_madden(
        self,
        existing: TeamGameSummary,
    ) -> TeamGameSummary:
        existing.schedule_id = self.scheduleId
        existing.week_index = self.weekIndex

        existing.def_forced_fum = self.defForcedFum
        existing.def_fum_rec = self.defFumRec
        existing.def_ints_rec = self.defIntsRec
        existing.def_pts_per_game = self.defPtsPerGame
        existing.def_pass_yds = self.defPassYds
        existing.def_rush_yds = self.defRushYds
        existing.def_red_zone_fgs = self.defRedZoneFGs
        existing.def_red_zones = self.defRedZones
        existing.def_red_zone_pct = self.defRedZonePct
        existing.def_red_zone_tds = self.defRedZoneTDs
        existing.def_sacks = self.defSacks
        existing.def_total_yds = self.defTotalYds

        existing.off_4th_down_att = self.off4thDownAtt
        existing.off_4th_down_conv = self.off4thDownConv
        existing.off_4th_down_conv_pct = self.off4thDownConvPct
        existing.off_fum_lost = self.offFumLost
        existing.off_ints_lost = self.offIntsLost
        existing.off_1st_downs = self.off1stDowns
        existing.off_pts_per_game = self.offPtsPerGame
        existing.off_pass_tds = self.offPassTDs
        existing.off_pass_yds = self.offPassYds
        existing.off_rush_tds = self.offRushTDs
        existing.off_rush_yds = self.offRushYds

        existing.off_red_zone_fgs = self.offRedZoneFGs
        existing.off_red_zones = self.offRedZones
        existing.off_red_zone_pct = self.offRedZonePct
        existing.off_red_zone_tds = self.offRedZoneTDs

        existing.off_sacks = self.offSacks

        existing.off_3rd_down_att = self.off3rdDownAtt
        existing.off_3rd_down_conv = self.off3rdDownConv
        existing.off_3rd_down_conv_pct = self.off3rdDownConvPct

        existing.off_2pt_att = self.off2PtAtt
        existing.off_2pt_conv = self.off2PtConv
        existing.off_2pt_conv_pct = self.off2PtConvPct

        existing.off_total_yds = self.offTotalYds
        existing.off_total_yds_gained = self.offTotalYdsGained

        existing.penalties = self.penalties
        existing.penalty_yds = self.penaltyYds

        existing.seed = self.seed
        existing.season_index = self.seasonIndex
        existing.stage_index = self.stageIndex

        existing.total_losses = self.totalLosses
        existing.total_ties = self.totalTies
        existing.total_wins = self.totalWins

        existing.to_diff = self.tODiff
        existing.to_giveaways = self.tOGiveaways
        existing.to_takeaways = self.tOTakeaways

        return existing


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
    throwAccDeepRating: int | None = None
    throwAccMidRating: int | None = None
    throwAccShortRating: int | None = None
    throwAwayTrait: int = 0
    throwPowerRating: int = 0
    throwOnRunRating: int = 0
    throwUnderPressureRating: int = 0
    teamId: int | None = None
    truckRating: int = 0
    teamSchemeOvr: int | None = None
    weight: int | None = None
    experiencePoints: int = 0
    yACCatchTrait: int = 0
    yearsPro: int | None = None
    zoneCoverRating: int = 0
    rosterId: int

    rosterGoalList: list[MaddenRosterGoal | None] = Field(default_factory=list)  # type: ignore


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


class MaddenLeagueInfoSetting(BaseModel):
    crossplayEnabled: bool
    legendsEnabled: bool
    leagueType: str
    maxMembers: int
    acceleratedClockEnabled: bool
    isPublic: bool
    quarterLength: int
    skillLevel: str
    leagueModeType: str


class MaddenLeagueInfo(BaseModel):
    lastAdvancedTimeSecs: int
    calendarYear: int
    numMembers: int
    commishPlatform: str
    commish: dict
    creationTime: int
    currentWeekCompleted: bool
    userFullName: str
    userPosition: str
    userTeamId: int
    importedLeagueId: int
    isImportable: bool
    isNextGameHome: bool
    isUsingUgc: bool
    joinsEnabled: bool
    leagueId: int
    leagueName: str
    nextOpponentTeamId: int
    rosterId: int
    settings: MaddenLeagueInfoSetting
    seasonSort: int
    seasonText: str
    secsSinceLastAdvancedTime: int
    teamLogos: str
    teams: str
    userPlayerClass: str
    userTeamLogoId: int
    userTeamName: str


class HubWeekInfo(BaseModel):
    gamesPlayedCount: int
    gamesPlayerStatsCount: int
    gameTotalCount: int
    stageIndex: int
    weekIndex: int
    weekTitle: str


class HubSeasonInfo(BaseModel):
    isAnnualAwardsPeriodActive: bool
    displayWeek: int
    calendarYear: int
    superBowlNumber: int
    isDraftScoutingActive: bool
    isDraftActive: bool
    isFreeAgentPeriodActive: bool
    isFantasyDraftActive: bool
    isGoalsPeriodActive: bool
    nextSeasonWeek: int
    offSeasonStage: int
    offSeasonWeekCount: int
    postSeasonWeekCount: int
    isProBowlPlayable: bool
    isPracticeSquadPeriodActive: bool
    preseasonWeekCount: int
    isReSignPeriodActive: bool
    regularSeasonWeekCount: int
    isDemandReleaseCoachAvailable: bool
    isInSeasonFreeAgentsAvailable: bool
    isLeagueStarted: bool
    maxYears: Literal[30]
    isDemandReleasePlayerAvailable: bool
    seasonWeek: int
    seasonWeekType: int
    seasonYear: int
    weekTitle: str
    seasonTitle: str
    totalSeasonWeekCount: int
    isWeeklyAwardsPeriodActive: bool


class ExportSizeEstimateInfo(BaseModel):
    defensiveStatsPerGameEstimate: int
    kickingStatsPerGameEstimate: int
    leagueTotalEstimate: int
    leagueTeamTotalEstimate: int
    rosterDataPerPlayerEstimate: int
    passingStatsPerGameEstimate: int
    puntingStatsPerGameEstimate: int
    receivingStatsPerGameEstimate: int
    rushingStatsPerGameEstimate: int
    scheduleDataPerGameEstimate: int
    standingsTotalEstimate: int
    teamStatsPerGameEstimate: int


class GameInfo(BaseModel):
    awayTeamPrimaryColorBlue: int
    awayTeamPrimaryColorGreen: int
    awayTeamPrimaryColorRed: int
    awayCityName: str
    awayTeamLogoId: int
    awayLoss: int
    awayName: str
    awayTie: int
    awayWin: int
    isByeWeek: bool
    gameTime: str
    displayedWeek: str
    forceWin: int
    homeLoss: int
    homeName: str
    homeTie: int
    homeWin: int
    matchup: str
    isGamePlayed: bool
    result: str
    week: int
    weekType: int
    homeTeamPrimaryColorBlue: int
    homeTeamPrimaryColorGreen: int
    homeTeamPrimaryColorRed: int
    homeCityName: str
    homeTeamLogoId: int
    awayUserId: int
    awayUserName: str
    homeUserId: int
    homeUserName: str
    isAwayHuman: bool
    isHomeHuman: bool
    numberTimesPlayed: int
    isBoxScoreUnavailable: bool
    awayTeam: int
    homeTeam: int


class LeagueSchedule(BaseModel):
    canForceWin: bool
    seasonGameKey: int
    seasonGameInfo: GameInfo


class GameScheduleHubInfo(BaseModel):
    userCanForceWin: bool
    leagueSchedule: list[LeagueSchedule]
    userTeam: int


class HubCareerInfo(BaseModel):
    isLeagueAutoSimming: bool
    isLeagueAdvancing: bool
    requestInfoList: list  # I dont know what this isssss
    seasonInfo: HubSeasonInfo


class HubPlayerCountInfo(BaseModel):
    freeAgentCount: int
    practiceSquadCount: int
    rosterCount: int
    totalCount: int


class HubTeamIdInfo(BaseModel):
    shortName: str
    displayName: str
    presentationId: int
    teamId: int


class UserAdminInfo(BaseModel):
    canEnableUnlimitedAutoPilot: bool
    isMasterUser: bool
    isAdmin: bool
    isDraftActive: bool
    isLeagueStarted: bool
    adminLevel: str
    canAdminsBootAdmins: bool
    userId: int
    canAdminsRemoveAdmins: bool


class UserInfo(BaseModel):
    defaultRequestActionTimeout: Literal["On", "Off"]
    autoPilot: bool
    characterName: str
    isCoach: bool
    isOwner: bool
    isOnline: bool
    position: int
    readyToAdvance: bool
    teamName: str
    userName: str
    isAdmin: bool
    showNFLPA: bool
    platformId: int
    portraitId: int
    salaryCapPenalty: int
    teamPrimaryColor: int
    team: int
    teamLogoId: int
    gameInfo: str
    adminLevel: str
    userAttribute: int
    durability: int
    userId: int
    intangible: int
    legacyScore: int
    overall: int
    production: int
    physical: int
    size: int


class HubUserAdminInfo(BaseModel):
    userAdminInfo: UserAdminInfo
    userInfoMap: dict[int, UserInfo]


class HubResponseValue(BaseModel):
    availableWeekInfoList: list[HubWeekInfo]
    careerHubInfo: HubCareerInfo
    exportSizeEstimateInfo: ExportSizeEstimateInfo
    gameScheduleHubInfo: GameScheduleHubInfo
    playerCountInfo: HubPlayerCountInfo
    message: str
    secsSinceLastAdvancedTime: int
    success: bool
    teamIdInfoList: list[HubTeamIdInfo]
    userAdminHubInfo: HubUserAdminInfo

    def get_week(self):
        return self.careerHubInfo.seasonInfo.displayWeek

    def get_year(self):
        return self.careerHubInfo.seasonInfo.calendarYear

    def get_internal_week_and_stage(self):
        week_index = self.careerHubInfo.seasonInfo.seasonWeek
        stage_index = self.careerHubInfo.seasonInfo.seasonWeekType
        return (week_index, stage_index)

    def get_human_game_summaries(self) -> list[HumanGameSummary]:
        summaries = []
        for user_info in self.userAdminHubInfo.userInfoMap.items():
            _, user = user_info
            game_summary: HumanGameSummary = {
                "user_name": user.userName,
                "summary": user.gameInfo,
            }
            id = user.userId
            user_game = next(
                (
                    game
                    for game in self.gameScheduleHubInfo.leagueSchedule
                    if game.seasonGameInfo.homeUserId == id
                    or game.seasonGameInfo.awayUserId == id
                ),
                None,
            )
            if user_game is not None and not user_game.seasonGameInfo.isGamePlayed:
                info = user_game.seasonGameInfo
                home_text = f"{info.homeCityName} ({info.homeWin}-{info.homeLoss}-{info.homeTie})"
                away_text = f"{info.awayCityName} ({info.awayWin}-{info.awayLoss}-{info.awayTie})"
                game_summary["summary"] = f"{home_text} @ {away_text}"

            summaries.append(game_summary)
        return summaries


class HubResponseInfo(BaseModel):
    tdfid: int
    tdfclass: str
    value: HubResponseValue


class MaddenLeagueHubInfo(BaseModel):
    responseInfo: HubResponseInfo
