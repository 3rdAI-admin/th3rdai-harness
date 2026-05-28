#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/.icm-helpers.sh"

echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║   Agent Harness — Configure Project Profile     ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "This writes _config/project-profile.md for project-level audience, tone, constraints, and quality preferences."
echo ""

load_project_path
mkdir -p "$PROJECT_PATH/_config"

step "Project audience and users"
read -rp "$(echo -e "${CYAN}?${NC} Who is this harness/project for?: ")" AUDIENCE
AUDIENCE="${AUDIENCE:-Developers and AI assistants working on agent/model workflows}"

step "Primary use cases"
echo -e "  ${DIM}Enter one use case per line. Press Enter on an empty line when done.${NC}"
USE_CASES=()
while true; do
  read -rp "  → " USE_CASE
  [ -z "$USE_CASE" ] && break
  USE_CASES+=("$USE_CASE")
done
if [ ${#USE_CASES[@]} -eq 0 ]; then
  USE_CASES=("Design reusable agents" "Version prompts" "Evaluate model and agent behavior" "Record validation evidence")
fi

step "Style and quality preferences"
read -rp "$(echo -e "${CYAN}?${NC} Preferred communication style [concise, explicit, evidence-based]: ")" STYLE
STYLE="${STYLE:-concise, explicit, evidence-based}"
read -rp "$(echo -e "${CYAN}?${NC} Risk tolerance [low/medium/high]: ")" RISK
RISK="${RISK:-low}"

step "Writing project profile"
{
  echo "# Project Profile"
  echo ""
  echo "## Audience"
  echo "$AUDIENCE"
  echo ""
  echo "## Primary Use Cases"
  for item in "${USE_CASES[@]}"; do
    echo "- $item"
  done
  echo ""
  echo "## Communication Style"
  echo "$STYLE"
  echo ""
  echo "## Risk Tolerance"
  echo "$RISK"
  echo ""
  echo "## Quality Preferences"
  echo "- Prefer explicit contracts over implied behavior."
  echo "- Keep agent, skill, prompt, model, eval, and run artifacts separate."
  echo "- Record assumptions, validation results, and skipped checks."
  echo "- Require human approval for destructive commands, dependency installation, and git commits."
} > "$PROJECT_PATH/_config/project-profile.md"

detail "Written: _config/project-profile.md"

if [ ! -f "$PROJECT_PATH/_config/brand-voice.md" ]; then
  cat > "$PROJECT_PATH/_config/brand-voice.md" <<'BV_EOF'
# Brand Voice

## Audience
See `_config/project-profile.md`.

## Tone
Concise, explicit, and evidence-based.

## Style
- Use clear headings.
- Prefer short paragraphs.
- Make assumptions visible.
- State validation status clearly.
BV_EOF
  detail "Written compatibility file: _config/brand-voice.md"
fi

step "Here's your project profile"
echo ""
echo -e "${DIM}────────────────────────────────────────${NC}"
cat "$PROJECT_PATH/_config/project-profile.md"
echo -e "${DIM}────────────────────────────────────────${NC}"
echo ""
ok "Project profile configured"
echo ""
echo -e "  ${CYAN}Next:${NC} Run ${BOLD}06-validate-workspace.sh${NC}."
echo ""
