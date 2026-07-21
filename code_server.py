import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import threading
import webbrowser

oauth_code = None
oauth_event = threading.Event()
server = None


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.capture_request()

    def do_POST(self):
        self.capture_request()

    def capture_request(self):
        global oauth_code, server

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
    server = HTTPServer(("127.0.0.1", 80), Handler)
    server.serve_forever()


def get_auth_code():
    global oauth_code
    url = f"https://accounts.ea.com/connect/auth?hide_create=true&release_type=prod&response_type=code&redirect_uri={REDIRECT_URL}&client_id=MCA_26_COMP_APP&machineProfileKey=444d362e8e067fe2&authentication_source=317239"

    oauth_code = None
    oauth_event.clear()

    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()

    webbrowser.open(url)
    oauth_event.wait()

    return oauth_code
