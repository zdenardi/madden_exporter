from services.slack_service import send_message, send_table


def test_send_message():
    didSend = send_message("I am a test message")
    assert didSend.status_code == 200


def test_send_table():
    didSend = send_table([""], [""])
    print(didSend)
