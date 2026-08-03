import os

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

APP_TOKEN = os.getenv("APP_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")

client = WebClient(BOT_TOKEN)


def send_message(message: str, channel_name: str = "test_madden_bot"):
    try:
        response = client.chat_postMessage(channel=f"#{channel_name}", text=message)
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


def send_table(
    headers: list[str], data: list[str], channel_name: str = "test_madden_bot"
):
    try:
        response = client.chat_postMessage(
            channel=channel_name,
            blocks=[
                {
                    "type": "table",
                    "rows": [
                        [
                            {
                                "type": "rich_text",
                                "elements": [
                                    {
                                        "type": "rich_text_section",
                                        "elements": [
                                            {
                                                "type": "text",
                                                "text": "User",
                                                "style": {"bold": True},
                                            }
                                        ],
                                    }
                                ],
                            },
                            {
                                "type": "rich_text",
                                "elements": [
                                    {
                                        "type": "rich_text_section",
                                        "elements": [
                                            {
                                                "type": "text",
                                                "text": "Home Team",
                                                "style": {"bold": True},
                                            }
                                        ],
                                    }
                                ],
                            },
                            {
                                "type": "rich_text",
                                "elements": [
                                    {
                                        "type": "rich_text_section",
                                        "elements": [
                                            {
                                                "type": "text",
                                                "text": "Away Team",
                                                "style": {"bold": True},
                                            }
                                        ],
                                    }
                                ],
                            },
                            {
                                "type": "rich_text",
                                "elements": [
                                    {
                                        "type": "rich_text_section",
                                        "elements": [
                                            {
                                                "type": "text",
                                                "text": "Score",
                                                "style": {"bold": True},
                                            }
                                        ],
                                    }
                                ],
                            },
                        ],
                        [
                            {
                                "type": "rich_text",
                                "elements": [
                                    {
                                        "type": "rich_text_section",
                                        "elements": [
                                            {"type": "text", "text": "Brinkofhumor"}
                                        ],
                                    }
                                ],
                            },
                            {
                                "type": "rich_text",
                                "elements": [
                                    {
                                        "type": "rich_text_section",
                                        "elements": [
                                            {"type": "text", "text": "Cardinals "},
                                            {
                                                "type": "text",
                                                "text": "(4-3)",
                                                "style": {"italic": True},
                                            },
                                        ],
                                    }
                                ],
                            },
                            {
                                "type": "rich_text",
                                "elements": [
                                    {
                                        "type": "rich_text_section",
                                        "elements": [
                                            {"type": "text", "text": "Seahawks "},
                                            {
                                                "type": "text",
                                                "text": "(3-4)",
                                                "style": {"italic": True},
                                            },
                                        ],
                                    }
                                ],
                            },
                            {
                                "type": "rich_text",
                                "elements": [
                                    {
                                        "type": "rich_text_section",
                                        "elements": [
                                            {"type": "text", "text": "24-17 "}
                                        ],
                                    }
                                ],
                            },
                        ],
                    ],
                }
            ],
        )
        return response

    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")
        # Also receive a corresponding status_code
        assert isinstance(e.response.status_code, int)
        print(f"Received a response status_code: {e.response.status_code}")
