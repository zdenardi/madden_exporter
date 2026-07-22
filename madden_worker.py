import os
import time
import requests

from dotenv import load_dotenv

load_dotenv()
SYNC_ENDPOINT = os.getenv("SYNC_ENDPOINT")
SYNC_INTERVAL = int(os.getenv("SYNC_INTERVAL", "3600"))
while True:
    try:
        print("Syncing...")
        requests.get(SYNC_ENDPOINT, timeout=30, verify=False)
    except Exception as e:
        print(e)
    time.sleep(SYNC_INTERVAL)
