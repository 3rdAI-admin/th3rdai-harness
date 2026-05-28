#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/.icm-helpers.sh"

echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║   Agent Harness — Customize CLAUDE.md           ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "CLAUDE.md tells AI assistants how to operate inside this agent/model harness."
echo ""

load_project_path

if [ ! -f "$PROJECT_PATH/CLAUDE.md" ]; then
  warn "No CLAUDE.md found at $PROJECT_PATH"
  echo "Run 01-create-project.sh first to set up the folder structure."
  exit 1
fi

PROJECT_NAME=$(basename "$PROJECT_PATH")

step "Let's customize your harness identity"
echo ""
read -rp "$(echo -e "${CYAN}?${NC} Project name [${DIM}$PROJECT_NAME${NC}]: ")" INPUT_NAME
PROJ="${INPUT_NAME:-$PROJECT_NAME}"
detail "Project name: $PROJ"

echo ""
echo -e "  ${DIM}What is the AI's role in this harness?${NC}"
echo -e "  ${DIM}Example: an AI assistant that designs, evaluates, and improves agent/model workflows${NC}"
echo ""
read -rp "$(echo -e "${CYAN}?${NC} AI's role: ")" ROLE
ROLE="${ROLE:-an AI assistant that designs, evaluates, and improves agent/model workflows}"
detail "Role: $ROLE"

RULES=(
  "Read FRAMEWORK.md before changing harness concepts"
  "Use CONTEXT.md to route work to the correct lifecycle stage"
  "Read relevant agent contracts before performing agent-specific work"
  "Separate agents, skills, prompts, models, evals, configs, runs, and telemetry"
  "Do not install dependencies, run destructive commands, or commit changes without explicit approval"
  "Record validation results and skipped checks honestly"
)

echo ""
echo -e "  ${DIM}Add extra always-follow rules? One per line. Press Enter on an empty line when done.${NC}"
while true; do
  read -rp "  → " RULE
  [ -z "$RULE" ] && break
  RULES+=("$RULE")
done

step "Writing CLAUDE.md"
{
  echo "# $PROJ"
  echo ""
  echo "## Identity"
  echo "You are $ROLE."
  echo ""
  echo "## Navigation"
  echo "This workspace is an AI agent/model development harness. Start with \`FRAMEWORK.md\`, then use \`CONTEXT.md\` to route work."
  echo ""
  echo "## Folder Map"
  echo "| Folder | Purpose |"
  echo "|--------|---------|"
  echo "| \`FRAMEWORK.md\` | Defines harness concepts and operating principles |"
  echo "| \`agents/\` | Agent contracts with roles, permissions, outputs, and handoffs |"
  echo "| \`skills/\` | Reusable workflows and command procedures |"
  echo "| \`prompts/\` | Versioned prompt templates and changelogs |"
  echo "| \`models/\` | Provider guidance and model selection notes |"
  echo "| \`configs/\` | Agent, model, routing, and tool profiles |"
  echo "| \`evals/\` | Rubrics, representative cases, and results |"
  echo "| \`stages/\` | Lifecycle stage contracts |"
  echo "| \`runs/\` | Execution records and experiment notes |"
  echo "| \`telemetry/\` | Run-log schema and observability conventions |"
  echo "| \`shared/\` | Cross-stage resources |"
  echo ""
  echo "## Rules"
  for r in "${RULES[@]}"; do
    echo "- $r"
  done
} > "$PROJECT_PATH/CLAUDE.md"

detail "Written: CLAUDE.md"

step "Here's your new CLAUDE.md"
echo ""
echo -e "${DIM}────────────────────────────────────────${NC}"
cat "$PROJECT_PATH/CLAUDE.md"
echo -e "${DIM}────────────────────────────────────────${NC}"
echo ""
ok "CLAUDE.md updated"
echo ""
echo -e "  ${CYAN}Next:${NC} Run ${BOLD}03-setup-routing.sh${NC} to refresh routing."
echo ""
