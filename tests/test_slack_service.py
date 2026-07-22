from services.slack_service import send_message


def test_send_message():
    didSend = send_message("I am a test message")
    assert didSend.status_code == 200
