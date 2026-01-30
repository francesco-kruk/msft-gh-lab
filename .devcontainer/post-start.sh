#!/usr/bin/env bash
set -euo pipefail

info() { printf "[post-start] %s\n" "$1"; }

if ! command -v azd >/dev/null 2>&1; then
  info "azd not found. Rebuild the devcontainer to install Azure tools."
  exit 0
fi

if ! az account show >/dev/null 2>&1; then
  info "Azure CLI not authenticated. Run: azd auth login (and az login if prompted)."
fi

env_count=0
if env_json=$(azd env list --output json 2>/dev/null); then
  env_count=$(python - <<'PY'
import json,sys
try:
  data=json.load(sys.stdin)
  print(len(data))
except Exception:
  print(0)
PY
)
fi

if [[ "$env_count" -eq 0 ]]; then
  info "No azd environment found. Create one with: azd env new <name>"
  exit 0
fi

frontend_uri=""
if env_values=$(azd env get-values --output json 2>/dev/null); then
  frontend_uri=$(python - <<'PY'
import json,sys
try:
  data=json.load(sys.stdin)
  print(data.get("FRONTEND_URI",""))
except Exception:
  print("")
PY
)
fi

if [[ -n "$frontend_uri" ]]; then
  info "Deployed app URL: $frontend_uri"
  info "View all outputs: azd env get-values"
else
  info "Environment exists but app not deployed yet. Run: azd up"
fi
