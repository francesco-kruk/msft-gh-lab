#!/usr/bin/env bash
set -euo pipefail

bold() { printf "\033[1m%s\033[0m\n" "$1"; }
info() { printf "[post-create] %s\n" "$1"; }
warn() { printf "[post-create] %s\n" "$1"; }

check_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    warn "Missing required command: $cmd"
    return 1
  fi
}

info "Validating toolchain..."
missing=0
for cmd in azd az docker node python; do
  if ! check_cmd "$cmd"; then
    missing=1
  fi
done

if ! command -v uv >/dev/null 2>&1; then
  info "Installing uv..."
  curl -Ls https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

if ! command -v uv >/dev/null 2>&1; then
  warn "uv is still missing. Restart the terminal or add ~/.local/bin to PATH."
fi

if [[ "$missing" -eq 1 ]]; then
  warn "One or more required tools are missing. Try rebuilding the devcontainer."
fi

if [[ "${DEVCONTAINER_INSTALL_DEPS:-}" == "1" ]]; then
  info "Installing backend dependencies (uv sync)..."
  (cd backend && uv sync)

  info "Installing frontend dependencies (npm ci)..."
  (cd frontend && npm ci)

  # Install test dependencies if tests folder exists
  if [[ -d "tests" && -f "tests/requirements.txt" ]]; then
    info "Installing test dependencies..."
    pip install -r tests/requirements.txt

    info "Installing Playwright browsers..."
    playwright install chromium --with-deps
  fi
else
  info "Dependency install skipped. Set DEVCONTAINER_INSTALL_DEPS=1 to auto-install."
fi

cat <<'EOF'

🚀 Codespaces Ready!

To deploy to Azure:
1. azd auth login
2. azd env new <environment-name>
3. azd env set AZURE_LOCATION <region>  # e.g., eastus
4. azd up

After deployment, find your app URL:
azd env get-values | grep FRONTEND_URI

For local development:
- Backend: cd backend && STORAGE_MODE=memory uv run uvicorn src.main:app --reload
- Frontend: cd frontend && npm run dev

To run E2E tests (after starting backend & frontend):
  cd tests && pytest e2e/test_devices.py -v

Note: Local backend requires Cosmos RBAC roles for your Azure user (or use STORAGE_MODE=memory).
EOF
