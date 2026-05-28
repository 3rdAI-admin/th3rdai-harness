#!/usr/bin/env bash
set -euo pipefail

GREEN='\033[0;32m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; DIM='\033[2m'; NC='\033[0m'

info()  { echo -e "${BLUE}ℹ${NC}  $1"; }
ok()    { echo -e "${GREEN}✔${NC}  $1"; }
warn()  { echo -e "${YELLOW}⚠${NC}  $1"; }
step()  { echo -e "\n${CYAN}━━━${NC} ${BOLD}$1${NC}"; }
detail(){ echo -e "   ${DIM}→ $1${NC}"; }

echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║   Agent Harness — Create Project Structure      ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "This will create a complete AI agent/model development harness."
echo ""

read -rp "$(echo -e "${CYAN}?${NC} Where should I create the project? (path): ")" PROJECT_PATH
PROJECT_PATH="${PROJECT_PATH/#\~/$HOME}"

if [ -z "$PROJECT_PATH" ]; then
  echo -e "${YELLOW}✗${NC} No path provided. Exiting."
  exit 1
fi

if [ -d "$PROJECT_PATH" ]; then
  warn "Folder already exists: $PROJECT_PATH"
  read -rp "$(echo -e "${CYAN}?${NC} Overwrite files in this folder? (y/N): ")" OVERWRITE
  if [[ ! "$OVERWRITE" =~ ^[Yy]$ ]]; then
    echo "Exiting. Choose a different path."
    exit 1
  fi
fi

PROJECT_NAME=$(basename "$PROJECT_PATH")
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "$PROJECT_PATH" > "$SCRIPT_DIR/.icm-project-path"
detail "Saved project path for subsequent scripts"

copy_file() {
  local src="$TEMPLATE_ROOT/$1"
  local dest="$PROJECT_PATH/$1"
  mkdir -p "$(dirname "$dest")"
  cp "$src" "$dest"
  detail "Written: $1"
}

copy_dir() {
  local src="$TEMPLATE_ROOT/$1"
  local dest="$PROJECT_PATH/$1"
  mkdir -p "$dest"
  cp -R "$src"/. "$dest"/ 
  detail "Copied: $1/"
}

step "Step 1/4 — Creating directory structure"
mkdir -p "$PROJECT_PATH"

for d in agents prompts models configs evals stages runs telemetry scripts shared _config skills; do
  mkdir -p "$PROJECT_PATH/$d"
  detail "Created: $d/"
done
ok "Folder structure created"

step "Step 2/4 — Copying canonical harness files"
for f in README.md FRAMEWORK.md CLAUDE.md CONTEXT.md VERSION2.md VERSION3.md; do
  [ -f "$TEMPLATE_ROOT/$f" ] && copy_file "$f"
done

for d in agents prompts models configs evals stages runs telemetry shared _config skills; do
  [ -d "$TEMPLATE_ROOT/$d" ] && copy_dir "$d"
done

for script_file in "$TEMPLATE_ROOT"/scripts/*.sh; do
  [ -f "$script_file" ] || continue
  f="scripts/$(basename "$script_file")"
  copy_file "$f"
done
[ -f "$TEMPLATE_ROOT/scripts/.icm-helpers.sh" ] && copy_file "scripts/.icm-helpers.sh"
chmod +x "$PROJECT_PATH/scripts"/*.sh 2>/dev/null || true
ok "Harness files copied"

step "Step 3/4 — Customizing project identity"
python3 - "$PROJECT_PATH/CLAUDE.md" "$PROJECT_NAME" <<'PY'
from pathlib import Path
import sys
path = Path(sys.argv[1])
name = sys.argv[2]
if path.exists():
    text = path.read_text()
    lines = text.splitlines()
    if lines and lines[0].startswith('# '):
        lines[0] = f'# {name}'
    path.write_text('\n'.join(lines) + '\n')
PY
detail "Updated CLAUDE.md project title"
ok "Project identity initialized"

step "Step 4/4 — Verifying structure"
if [ -x "$PROJECT_PATH/scripts/07-validate-harness.sh" ]; then
  PROJECT_ROOT="$PROJECT_PATH" "$PROJECT_PATH/scripts/07-validate-harness.sh"
else
  warn "Validation script was not copied"
fi

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   ✅  Agent harness created successfully!        ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${BOLD}Location:${NC} $PROJECT_PATH"
echo -e "  ${BOLD}Files:${NC}    $(find "$PROJECT_PATH" -type f | wc -l | tr -d ' ') files in $(find "$PROJECT_PATH" -type d | wc -l | tr -d ' ') folders"
echo ""
echo -e "  ${CYAN}Next steps:${NC}"
echo -e "  1. Review ${BOLD}CLAUDE.md${NC} and ${BOLD}FRAMEWORK.md${NC}"
echo -e "  2. Configure ${BOLD}configs/models.yaml${NC} for your preferred providers"
echo -e "  3. Add or revise agents in ${BOLD}agents/${NC}"
echo -e "  4. Run ${BOLD}scripts/07-validate-harness.sh${NC} before release"
echo ""
