from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum


class Status(Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"


@dataclass
class Entitlement:
    entitlementId: str
    entitlementSource: str
    entitlementTag: str
    entitlementType: str
    grantDate: date
    groupName: str
    productCatalog: str
    productId: str
    projectId: str
    statusReasonCode: str
    status: Status
    terminationDate: str
    useCount: int
    isConsumable: bool
    pidUri: str
    originPermissions: str
    version: int
    lastModifidedDate: datetime


@dataclass
class Persona:
    personaId: int
    pidId: int
    displayName: str
    name: str
    namespaceName: str
    isVisible: bool
    status: Status
    statusReasonCode: str
    showPersona: str
    dateCreated: datetime
    lastAuthenticated: datetime


@dataclass
class AccessTokenResponse:
    access_token: str
    token_type: str  # Bearer
    expires_in: int
    refresh_token: str
    id_token: None


@dataclass
class EAIds:
    originPersonaName: str
    nucleusAccountId: str
    originPersonaId: str


@dataclass
class ExternalIds:
    psnAccountId: int
    steamAccountId: int
    switchId: int
    xblAccountId: int


@dataclass
class PlatformInfo:
    clientPlatform: str  # xbsx
    eaIds: EAIds
    externalIds: ExternalIds


@dataclass
class PersonDetails:
    displayName: str
    lastAuthenticated: int
    personaIa: int
    status: str
    extId: int


@dataclass
class UserLoginInfo:
    isFirstConsoleLogin: bool
    platformInfo: PlatformInfo
    blazeId: int
    isFirstLogin: bool
    geoIpSucceeded: bool
    sessionKey: str
    lastLoginDateTime: int
    previousAnonymousAccountId: int
    personDetails: PersonDetails
    accountId: int


@dataclass
class BlazeSession:
    blaze_id: str
    session_key: str
    request_id: int


@dataclass
class AuthData:
    auth_data: str
    auth_code: str
    auth_type: int


@dataclass
class TokenInformation:
    accessToken: str
    refreshToken: str
    expiry: date
    console: str
    blazeId: str


@dataclass
class BlazeReq:
    commandName: str
    componentId: int
    commandId: int
    requestPayload: {str, any}
    componentName: str


@dataclass
class HumanGameSummary:
    user_name: str
    summary: str


@dataclass
class WeekInformation:
    advanced: bool
    old_week: int | None
    current_week: int
    old_year: int | None
    current_year: int
    did_summaries_update: bool
    summaries: str
    week_index: int
    stage_index: int
    season_index: int

    @property
    def season_changed(self) -> bool:
        return self.old_year is not None and self.old_year != self.current_year

    @property
    def week_changed(self) -> bool:
        return self.old_week is not None and self.old_week != self.current_week

    @property
    def was_created(self) -> bool:
        return self.old_week is None and self.advanced
