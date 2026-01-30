#!/usr/bin/env bash
set -euo pipefail

info() { printf "[azd-up] %s\n" "$1"; }
error() { printf "[azd-up] %s\n" "$1" >&2; }

if ! command -v azd >/dev/null 2>&1; then
  error "azd is not installed. Rebuild the devcontainer."
  exit 1
fi

if ! az account show >/dev/null 2>&1; then
  error "Azure CLI not authenticated. Run: azd auth login (and az login if prompted)."
  exit 1
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
  error "No azd environment found. Create one with: azd env new <name>"
  exit 1
fi

location=""
if env_values=$(azd env get-values --output json 2>/dev/null); then
  location=$(python - <<'PY'
import json,sys
try:
  data=json.load(sys.stdin)
  print(data.get("AZURE_LOCATION",""))
except Exception:
  print("")
PY
)
fi

if [[ -z "$location" ]]; then
  error "AZURE_LOCATION is not set. Run: azd env set AZURE_LOCATION <region>"
  exit 1
fi

info "Running azd up..."
azd up "$@"

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
  info "Deployment complete. Frontend URL: $frontend_uri"
else
  info "Deployment complete. View outputs with: azd env get-values"
fi
