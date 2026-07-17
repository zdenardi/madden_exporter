from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

APP_TOKEN = "***REMOVED***"
BOT_TOKEN = "***REMOVED***"
client = WebClient(BOT_TOKEN)


def send_message(message: str):
    try:
        response = client.chat_postMessage(channel="#test_madden_bot", text=message)
        assert response["message"]["text"] == message
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")
        # Also receive a corresponding status_code
        assert isinstance(e.response.status_code, int)
        print(f"Received a response status_code: {e.response.status_code}")
    return response
