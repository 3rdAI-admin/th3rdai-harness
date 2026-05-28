#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/.icm-helpers.sh"
TEMPLATE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║   Agent Harness — Refresh Stage Contracts       ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "This refreshes the seven lifecycle stage CONTEXT.md contracts."
echo ""

load_project_path

STAGES=(
  "01-task-definition"
  "02-agent-design"
  "03-prompt-design"
  "04-tool-integration"
  "05-evaluation"
  "06-iteration"
  "07-release"
)

step "Ensuring lifecycle stage folders"
for stage in "${STAGES[@]}"; do
  mkdir -p "$PROJECT_PATH/stages/$stage/output"
  if [ -f "$TEMPLATE_ROOT/stages/$stage/CONTEXT.md" ]; then
    cp "$TEMPLATE_ROOT/stages/$stage/CONTEXT.md" "$PROJECT_PATH/stages/$stage/CONTEXT.md"
    detail "Refreshed: stages/$stage/CONTEXT.md"
  else
    warn "Template missing: stages/$stage/CONTEXT.md"
  fi
done

ok "Lifecycle stage contracts refreshed"
echo ""
echo -e "  ${CYAN}Stages:${NC}"
for stage in "${STAGES[@]}"; do
  echo -e "    ${GREEN}✔${NC} stages/$stage/"
done
echo ""
echo -e "  ${CYAN}Next:${NC} Run ${BOLD}06-validate-workspace.sh${NC}."
echo ""
