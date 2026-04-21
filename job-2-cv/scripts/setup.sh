#!/usr/bin/env bash
# Set up the local Python venv + Playwright for the job-2-cv skill.
# Idempotent: safe to re-run. Runs in the current working directory.

set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found on PATH. Install Python 3 first (e.g. 'brew install python')." >&2
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "Creating .venv/ ..."
  python3 -m venv .venv
else
  echo ".venv/ already exists, reusing."
fi

VENV_PY=".venv/bin/python"
VENV_PIP=".venv/bin/pip"

"$VENV_PY" -m pip install --upgrade pip >/dev/null

if ! "$VENV_PY" -c "import playwright" 2>/dev/null; then
  echo "Installing playwright into .venv/ ..."
  "$VENV_PIP" install playwright
else
  echo "playwright already installed in .venv/."
fi

# Install the Chromium binary Playwright uses. Cached at ~/Library/Caches/ms-playwright/
# on macOS, so this is typically a no-op on re-run.
echo "Ensuring Chromium is installed for Playwright ..."
"$VENV_PY" -m playwright install chromium

echo "Setup complete. Use: .venv/bin/python <skill>/scripts/render.py <file>.html"
