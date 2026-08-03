import base64
import hashlib
import json
import secrets
import ssl
import threading
import time
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import requests
import urllib3
from sqlalchemy import select
from sqlalchemy.orm import Session

from constants import (
    AUTH_SOURCE,
    CLIENT_ID,
    CLIENT_SECRET,
    LEAGUE_ID,
    MACHINE_KEY,
    REDIRECT_URL,
    LeagueData,
    LeagueDataKey,
)
from data_classes.data_classes import (
    AccessTokenResponse,
    AuthData,
    BlazeReq,
    BlazeSession,
    Entitlement,
    Persona,
    TokenInformation,
    UserLoginInfo,
)
from data_classes.madden_classes import (
    MaddenLeagueHubInfo,
    MaddenLeagueInfo,
    MaddenStandingsEntry,
    MaddenTeam,
)
from models.EAtoken import EATokenInfo

oauth_code = None
oauth_event = threading.Event()
server = None


class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    # "Transport adapter" that allows us to use custom ssl_context.

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context,
        )


def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount("https://", CustomHttpAdapter(ctx))
    return session


def get_EA_access_token(code: str):

    URL = "https://accounts.ea.com/connect/token"
    HEADERS = {
        "Accept-Charset": "UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; sdk_gphone_x86_64 Build/TE1A.220922.031)",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip",
    }

    PARAMS = {
        "authentication_source": AUTH_SOURCE,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URL,
        "release_type": "prod",
        "client_id": CLIENT_ID,
    }
    response = requests.post(URL, headers=HEADERS, params=PARAMS)

    if not response.ok:
        print(f"Failed to use login code ${response.text()}")

    access_token: AccessTokenResponse = response.json()
    return access_token


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.capture_request()

    def do_POST(self):
        self.capture_request()

    def capture_request(self):
        global oauth_code

        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        oauth_code = query.get("code", [None])[0]

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8", errors="replace")

        log = {
            "timestamp": datetime.now().isoformat(),
            "client": self.client_address[0],
            "method": self.command,
            "url": self.path,
            "path": parsed.path,
            "query": parse_qs(parsed.query),
            "headers": dict(self.headers),
            "body": body,
        }

        print(json.dumps(log, indent=4))

        with open(
            f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "w",
        ) as f:
            json.dump(log, f, indent=4)

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        self.wfile.write(b"""
        <html>
            <body>
                Login successful.<br>
                You can close this tab.
            </body>
        </html>
        """)

        if oauth_code:
            print("Captured Code: ", oauth_code)
            oauth_event.set()

            self.server.shutdown()


def run_server():
    global server
    server = HTTPServer(("0.0.0.0", 5001), Handler)
    server.serve_forever()


def get_auth_code():
    global oauth_code
    url = f"https://accounts.ea.com/connect/auth?hide_create=true&release_type=prod&response_type=code&redirect_uri={REDIRECT_URL}&client_id=MCA_26_COMP_APP&machineProfileKey=444d362e8e067fe2&authentication_source=317239"

    oauth_code = None
    oauth_event.clear()

    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()

    webbrowser.open(url=url)
    oauth_event.wait()

    return oauth_code


def get_personas(token: AccessTokenResponse):
    url = f"https://accounts.ea.com/connect/tokeninfo?access_token={token['access_token']}"
    headers = {
        "Accept-Charset": "UTF-8",
        "X-Include-Deviceid": "true",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; sdk_gphone_x86_64 Build/TE1A.220922.031)",
        "Accept-Encoding": "gzip",
    }
    response = requests.get(url, headers=headers)
    if not response.ok:
        print("Error Getting PID")
    pid_id = response.json()["pid_id"]
    pid_uri_url = f"https://gateway.ea.com/proxy/identity/pids/{pid_id}/entitlements/?status=ACTIVE"
    pid_headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; sdk_gphone_x86_64 Build/TE1A.220922.031)",
        "Accept-Charset": "UTF-8",
        "X-Expand-Results": "true",
        "Accept-Encoding": "gzip",
        "Authorization": f"Bearer {token['access_token']}",
    }
    pid_uri_response = requests.get(pid_uri_url, headers=pid_headers)
    if not pid_uri_response.ok:
        print("PID_URI Error")
    entitlements: list[Entitlement] = pid_uri_response.json()["entitlements"][
        "entitlement"
    ]
    valid_entitlements = [e for e in entitlements if e["status"] == "ACTIVE"]
    if not valid_entitlements:
        print("No active entitlements found")
    urls = [
        f"https://gateway.ea.com/proxy/identity{e['pidUri']}/personas?status=ACTIVE&access_token={token['access_token']}"
        for e in valid_entitlements
    ]
    session = requests.Session()

    def fetch(url):
        headers = {
            "Accept-Charset": "UTF-8",
            "X-Expand-Results": "true",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; sdk_gphone_x86_64 Build/TE1A.220922.031)",
            "Accept-Encoding": "gzip",
        }

        response = session.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def process_responses(urls: list[str]) -> list[Persona]:
        with ThreadPoolExecutor() as executor:
            responses = list(executor.map(fetch, urls))
        return responses[0]["personas"]["persona"]

    return process_responses(urls)


def get_persona_auth_code(access_token: str, persona: Persona):
    url = "https://accounts.ea.com/connect/auth"

    params = {
        "hide_create": "true",
        "release_type": "prod",
        "response_type": "code",
        "redirect_uri": REDIRECT_URL,
        "client_id": CLIENT_ID,
        "machineProfileKey": MACHINE_KEY,
        "authentication_source": AUTH_SOURCE,
        "access_token": access_token,
        "persona_id": persona["personaId"],
        "persona_namespace": persona["namespaceName"],
    }

    headers = {
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 13; sdk_gphone_x86_64 "
            "Build/TE1A.220922.031; wv) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.71 "
            "Mobile Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,image/apng,*/*;q=0.8,"
            "application/signed-exchange;v=b3;q=0.9"
        ),
        "X-Requested-With": "com.ea.gp.madden19companionapp",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        allow_redirects=False,
    )

    location = response.headers.get("Location")

    if not location:
        raise Exception("No redirect location returned")

    return extract_code(location)


def get_EA_jws_token(code: str):
    URL = "https://accounts.ea.com/connect/token"
    HEADERS = {
        "Accept-Charset": "UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; sdk_gphone_x86_64 Build/TE1A.220922.031)",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip",
    }

    PARAMS = {
        "authentication_source": AUTH_SOURCE,
        "client_secret": CLIENT_SECRET,
        "token_format": "JWS",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URL,
        "release_type": "prod",
        "client_id": CLIENT_ID,
    }
    response = requests.post(URL, headers=HEADERS, params=PARAMS)

    if not response.ok:
        print(f"Failed to use login code ${response.text()}")

    access_token: AccessTokenResponse = response.json()
    return access_token


def get_blaze_session(token: EATokenInfo) -> BlazeSession:

    year = 2026
    url = "https://wal2.tools.gos.bio-iad.ea.com/wal/authentication/login"
    headers = {
        "Accept-Charset": "UTF-8",
        "Accept": "application/json",
        "X-BLAZE-ID": f"madden-{year}-xbsx",
        "X-BLAZE-VOID-RESP": "XML",
        "X-Application-Key": "MADDEN-MCA",
        "Content-Type": "application/json",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; sdk_gphone_x86_64 Build/TE1A.220922.031)",
    }
    payload = {
        "accessToken": token.access_token,
        "productName": f"madden-{year}-xbsx-mca",
    }
    session = get_legacy_session()

    response = session.post(
        url,
        headers=headers,
        json=payload,
    )
    user_login_info: UserLoginInfo = response.json()["userLoginInfo"]

    blaze_id = user_login_info["blazeId"]
    session_key = user_login_info["sessionKey"]
    request_id = 1

    return BlazeSession(blaze_id, session_key, request_id)


def extract_code(location):
    parsed = urlparse(location)
    return parse_qs(parsed.query)["code"][0]


def calc_message_auth_data(session: BlazeSession):
    rand_4_bytes = secrets.token_bytes(4)
    req_data = json.dumps(
        {
            "staticData": "05e6a7ead5584ab4",
            "requestId": session.request_id,
            "blazeId": session.blaze_id,
        },
        separators=(",", ":"),
    )
    secret = "634203362017bf72f70ba900c0aa4e6b"  # from EA
    static_bytes = bytes.fromhex(secret)

    md5 = hashlib.md5()
    md5.update(rand_4_bytes)
    md5.update(static_bytes)
    xor_hash = md5.digest()

    request_buffer = bytes(req_data, "utf-8")
    scrambled_bytes = bytes(
        b ^ xor_hash[i % len(xor_hash)] for i, b in enumerate(request_buffer)
    )

    auth_data_bytes = rand_4_bytes + scrambled_bytes
    auth_code_from_EA = "3a53413521464c3b6531326530705b70203a2900"  # from EA
    static_auth_code = bytes.fromhex(auth_code_from_EA)

    auth_md5 = hashlib.md5()
    auth_md5.update(static_auth_code + auth_data_bytes)
    auth_digest = auth_md5.digest()
    auth_code = base64.b64encode(auth_digest).decode("utf-8")
    auth_data = base64.b64encode(auth_data_bytes).decode("utf-8")
    auth_type = 17039361  # From Ea
    return AuthData(auth_data, auth_code, auth_type)


def send_blaze_req(token: TokenInformation, session: BlazeSession, req: BlazeReq):
    headers = {
        "Accept-Charset": "UTF-8",
        "Accept": "application/json",
        "X-BLAZE-ID": "madden-2026-xbsx",
        "X-BLAZE-VOID-RESP": "XML",
        "X-Application-Key": "MADDEN-MCA",
        "Content-Type": "application/json",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; sdk_gphone_x86_64 Build/TE1A.220922.031)",
    }

    auth_data = calc_message_auth_data(session)
    message_expiration = int(time.time())
    request_payload = req["requestPayload"]
    rest = {k: v for k, v in req.items() if k != "requestPayload"}
    body = {
        "apiVersion": 2,
        "clientDevice": 3,
        "requestInfo": json.dumps(
            {
                **rest,
                "messageAuthData": {
                    "authData": auth_data.auth_data,
                    "authCode": auth_data.auth_code,
                    "authType": auth_data.auth_type,
                },
                "messageExpirationTime": message_expiration,
                "deviceId": MACHINE_KEY,
                "ipAddress": "127.0.0.1",
                "requestPayload": json.dumps(request_payload),
            }
        ),
    }

    url = f"https://wal2.tools.gos.bio-iad.ea.com/wal/mca/Process/{session.session_key}"
    response = requests.post(url=url, headers=headers, json=body, verify=False)

    return response


def get_export_data(
    token: TokenInformation,
    session: BlazeSession,
    export_type: LeagueDataKey,
    body: {str, any},
    retries=5,
    base_delay=1000,
):
    headers = {
        "Accept-Charset": "UTF-8",
        "Accept": "application/json",
        "X-BLAZE-ID": "madden-2026-xbsx",
        "X-BLAZE-VOID-RESP": "XML",
        "X-Application-Key": "MADDEN-MCA",
        "Content-Type": "application/json",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; sdk_gphone_x86_64 Build/TE1A.220922.031)",
    }
    url = f"https://wal2.tools.gos.bio-iad.ea.com/wal/mca/{LeagueData[export_type]}/{session.session_key}"
    response = requests.post(url=url, headers=headers, json=body, verify=False)
    return response


def refresh_token(refresh_token: str) -> TokenInformation:

    url = "https://accounts.ea.com/connect/token"
    headers = {
        "Accept-Charset": "UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; sdk_gphone_x86_64 Build/TE1A.220922.031)",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip",
    }
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "release_type": "prod",
        "authentication_source": AUTH_SOURCE,
        "refresh_token": refresh_token,
        "token_format": "JWS",
    }

    response = requests.post(url=url, headers=headers, data=data)
    return response.json()


def get_EA_token_info(session: Session):
    token = session.scalar(statement=select(EATokenInfo))
    if token is None:
        code = get_auth_code()
        t = get_EA_access_token(code)
        personas = get_personas(t)
        persona = personas[0]
        p_code = get_persona_auth_code(t["access_token"], persona)
        ea_jws = get_EA_jws_token(p_code)
        token = EATokenInfo(
            access_token=ea_jws["access_token"],
            refresh_token=ea_jws["refresh_token"],
            expires_at=datetime.now(timezone.utc)
            + timedelta(seconds=ea_jws["expires_in"]),
        )
        session.add(token)
    else:

        if token.expires_at <= datetime.now(timezone.utc) + timedelta(seconds=30):
            t = refresh_token(token.refresh_token)
            token.access_token = t["access_token"]
            token.refresh_token = t["refresh_token"]
            token.expires_at = datetime.now(timezone.utc)
            +timedelta(seconds=t["expires_in"])

    session.commit()
    session.refresh(token)
    token_info = EATokenInfo(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        expires_at=token.expires_at,
    )
    return token_info


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
        raise Exception["Error getting leagues"]


def get_teams(token: TokenInformation, session: BlazeSession, league_id: int):
    response = get_export_data(token, session, "TEAMS", {"leagueId": LEAGUE_ID})
    if response.ok and response.json()["leagueTeamInfoList"]:
        teams: list[MaddenTeam] = response.json()["leagueTeamInfoList"]
        return teams
    else:
        raise Exception["Error getting teams"]


def get_standings(token: TokenInformation, session: BlazeSession, league_id: int):
    response = get_export_data(token, session, "STANDINGS", {"leagueId": LEAGUE_ID})
    if response.ok and response.json()["teamStandingInfoList"]:
        standings: list[MaddenStandingsEntry] = response.json()["teamStandingInfoList"]
        return standings
    else:
        raise Exception["Error getting standings"]
