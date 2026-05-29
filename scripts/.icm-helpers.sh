#!/usr/bin/env bash
# Shared helpers for th3rdai-harness setup scripts

GREEN='\033[0;32m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; DIM='\033[2m'; NC='\033[0m'

info()  { echo -e "${BLUE}ℹ${NC}  $1"; }
ok()    { echo -e "${GREEN}✔${NC}  $1"; }
warn()  { echo -e "${YELLOW}⚠${NC}  $1"; }
step()  { echo -e "\n${CYAN}━━━${NC} ${BOLD}$1${NC}"; }
detail(){ echo -e "   ${DIM}→ $1${NC}"; }

# Load project path from config saved by step 01,
# or fall back to asking the user.
load_project_path() {
  local SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[1]}")" && pwd)"
  local CONFIG_FILE="$SCRIPT_DIR/.icm-project-path"

  if [ -f "$CONFIG_FILE" ]; then
    PROJECT_PATH="$(cat "$CONFIG_FILE")"
    PROJECT_PATH="${PROJECT_PATH/#\~/$HOME}"
    if [ -d "$PROJECT_PATH" ]; then
      ok "Using project: ${BOLD}$PROJECT_PATH${NC}"
      return 0
    else
      warn "Saved path not found: $PROJECT_PATH"
    fi
  fi

  # Fallback: ask the user
  read -rp "$(echo -e "${CYAN}?${NC} Path to your harness project folder: ")" PROJECT_PATH
  PROJECT_PATH="${PROJECT_PATH/#\~/$HOME}"

  if [ ! -d "$PROJECT_PATH" ]; then
    echo -e "${YELLOW}✗${NC} Directory not found: $PROJECT_PATH"
    echo "Run 01-create-project.sh first."
    exit 1
  fi

  # Save for next scripts
  echo "$PROJECT_PATH" > "$CONFIG_FILE"
  ok "Found project at: $PROJECT_PATH"
}
