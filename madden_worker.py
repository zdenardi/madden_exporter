import time
import requests

while True:
    try:
        requests.get("http://app:5000/sync_league", timeout=30)
    except Exception as e:
        print(e)
    time.sleep(3600)
