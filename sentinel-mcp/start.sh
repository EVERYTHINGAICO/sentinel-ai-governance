#!/bin/bash
# SENTINEL — Full stack startup (Linux / Mac / WSL)
# Run from repo root: bash sentinel-mcp/start.sh

set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cleanup() {
  echo ""
  echo "  Shutting down..."
  kill $(jobs -p) 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo ""
echo "  SENTINEL — Starting full stack"
echo ""

echo "  [1/3] Mock LLM backend on :18000..."
python3 "$ROOT/research/governance-suite/scripts/mock_openai_backend.py" &
sleep 1

echo "  [2/3] Lobster Trap proxy on :8080..."
"$ROOT/lobstertrap/lobstertrap" serve \
  --policy "$ROOT/lobstertrap/configs/default_policy.yaml" \
  --listen :8080 \
  --backend http://localhost:18000 &
sleep 2

echo "  [3/3] SENTINEL governance server on :5001..."
echo ""
python3 "$ROOT/sentinel-mcp/api_server.py"
