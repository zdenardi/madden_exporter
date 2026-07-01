#!/usr/bin/env bash

set -euo pipefail

PORT=5000
TUNNEL_FILE="tunnel_url.txt"

if ! command -v cloudflared >/dev/null 2>&1; then
    echo "cloudflared is not installed."
    echo "Install it with:"
    echo "  brew install cloudflared"
    exit 1
fi

echo "Starting Cloudflare tunnel..."

LOGFILE=$(mktemp)

cloudflared tunnel --url "http://localhost:${PORT}" \
    >"$LOGFILE" 2>&1 &

TUNNEL_PID=$!

cleanup() {
    echo
    echo "Stopping tunnel..."
    kill "$TUNNEL_PID" 2>/dev/null || true
    rm -f "$LOGFILE"
}

trap cleanup EXIT INT TERM

echo "Waiting for tunnel..."

URL=""
until [[ -n "$URL" ]]; do
    URL=$(grep -oE 'https://[-a-zA-Z0-9]+\.trycloudflare\.com' "$LOGFILE" | head -1 || true)
    sleep 1
done


echo
echo "========================================"
echo "Tunnel ready!"
echo "$URL"
echo "========================================"
echo

wait "$TUNNEL_PID"

