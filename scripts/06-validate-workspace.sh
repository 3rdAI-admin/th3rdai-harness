#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/.icm-helpers.sh"

echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║   Agent Harness — Validate Workspace            ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""

load_project_path

if [ ! -x "$SCRIPT_DIR/07-validate-harness.sh" ]; then
  warn "scripts/07-validate-harness.sh is missing or not executable."
  exit 1
fi

PROJECT_ROOT="$PROJECT_PATH" "$SCRIPT_DIR/07-validate-harness.sh"
