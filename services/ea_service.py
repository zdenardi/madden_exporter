import requests

AUTH_SOURCE = 317239
CLIENT_SECRET = (
    "teJpJ9cSXFqZAuKNW8IuHpy8D4dwWPoVrPoek38iCnrGbrUSfjqnHMBAv8iCVjeSm_20250910175618"
)
CODE = "QUOxAHEsvIEb2_bi1j5qbYY4ft4Jx2DGndz-GE6cAQ"
REDIRECT_URL = "http://127.0.0.1/success"
CLIENT_ID = "MCA_26_COMP_APP"
MACHINE_KEY = "444d362e8e067fe2"
EA_LOGIN_URL = f"https://accounts.ea.com/connect/auth?hide_create=true&release_type=prod&response_type=code&redirect_uri=${REDIRECT_URL}&client_id=${CLIENT_ID}&machineProfileKey=${MACHINE_KEY}&authentication_source=${AUTH_SOURCE}"


def get_EA_access_token():
    URL = "https://accounts.ea.com/connect/token"
    HEADERS = (
        {
            "Accept-Charset": "UTF-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; sdk_gphone_x86_64 Build/TE1A.220922.031)",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Encoding": "gzip",
        },
    )
    PARAMS = {
        "authentication_source": AUTH_SOURCE,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": CODE,
        "redirect_uri": REDIRECT_URL,
        "release_type": "prod",
        "client_id": CLIENT_ID,
    }
    response = requests.post(URL, headers=HEADERS, params=PARAMS)

    if not response.ok():
        print(f"Failed to use login code ${response.text()}")

    access_token = response.json()["access_token"]
    return access_token
