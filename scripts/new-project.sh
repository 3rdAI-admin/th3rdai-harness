#!/usr/bin/env bash
set -euo pipefail

# new-project.sh — install the AI Agent Development Harness into an existing
# app/repo as a segmented subfolder (default: harness/), wire it to orchestrate
# that app, seed an initial task, and hand off to the /plan process.
#
# This is the first step for using the harness against an existing codebase.
# It delegates the folder-tree copy to scripts/01-create-project.sh (single
# source of truth), then layers on app detection, a deployment overlay, a
# seeded task, and a /plan handoff marker.

GREEN='\033[0;32m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; DIM='\033[2m'; NC='\033[0m'

info()  { echo -e "${BLUE}ℹ${NC}  $1"; }
ok()    { echo -e "${GREEN}✔${NC}  $1"; }
warn()  { echo -e "${YELLOW}⚠${NC}  $1"; }
step()  { echo -e "\n${CYAN}━━━${NC} ${BOLD}$1${NC}"; }
detail(){ echo -e "   ${DIM}→ $1${NC}"; }

WITH_ORCHESTRATOR=0
TARGET_ARG=""
while [ $# -gt 0 ]; do
  case "$1" in
    --with-orchestrator) WITH_ORCHESTRATOR=1; shift ;;
    -h|--help)
      cat <<'EOF'
Usage: scripts/new-project.sh [target-repo-path] [--with-orchestrator]
       ./new-project.sh        [target-repo-path] [--with-orchestrator]   (root symlink)

Installs the harness into an existing app/repo as a segmented subfolder
(default: harness/), records what app it orchestrates, seeds an initial task
from a one-line goal, and hands off to /plan.

Arguments:
  target-repo-path        Path to the app repo root (default: current directory)

Options:
  --with-orchestrator     Include the Native Orchestrator CLI, tests, eval cases

Environment (non-interactive):
  HARNESS_TARGET_REPO     Target app root (overrides positional argument)
  HARNESS_SUBDIR          Subfolder name to install into (default: harness)
  HARNESS_PROJECT_GOAL    One-line project goal (skips the goal prompt)
  HARNESS_OVERWRITE=1     Overwrite the harness subfolder if it already exists

Next step:
  The harness 'new-project' skill auto-continues into /plan using the seeded
  task. A human can run the printed /plan command instead.
EOF
      exit 0
      ;;
    -*) echo "Unknown option: $1" >&2; exit 1 ;;
    *) TARGET_ARG="$1"; shift ;;
  esac
done

echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║   Agent Harness — Install Into Existing Repo    ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "This installs the harness into a segmented subfolder of your app"
echo -e "and hands off to the ${BOLD}/plan${NC} process to start development."
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Resolve the delegate whether this script lives in scripts/ or at the repo root
# (e.g. invoked via a root-level symlink: new-project.sh -> scripts/new-project.sh).
DELEGATE=""
for cand in "$SCRIPT_DIR/01-create-project.sh" "$SCRIPT_DIR/scripts/01-create-project.sh"; do
  if [ -f "$cand" ]; then DELEGATE="$cand"; break; fi
done
if [ -z "$DELEGATE" ]; then
  echo -e "${YELLOW}✗${NC} Cannot find 01-create-project.sh (looked in $SCRIPT_DIR and $SCRIPT_DIR/scripts)." >&2
  exit 1
fi

# --- Step 1/8 — Resolve target + install paths ---------------------------------
step "Step 1/8 — Resolving paths"

TARGET="${HARNESS_TARGET_REPO:-${TARGET_ARG:-$(pwd)}}"
TARGET="${TARGET/#\~/$HOME}"
if [ ! -d "$TARGET" ]; then
  echo -e "${YELLOW}✗${NC} Target repo path does not exist: $TARGET" >&2
  exit 1
fi
TARGET="$(cd "$TARGET" && pwd)"        # absolute
APP_NAME="$(basename "$TARGET")"
SUBDIR="${HARNESS_SUBDIR:-harness}"
INSTALL_DIR="$TARGET/$SUBDIR"

detail "Target app:   $TARGET"
detail "App name:     $APP_NAME"
detail "Install into: $INSTALL_DIR"

if git -C "$TARGET" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  detail "Git repo:     yes"
else
  detail "Git repo:     no (informational only)"
fi

# --- Step 2/8 — Overwrite pre-check (before goal prompt) -----------------------
step "Step 2/8 — Checking install location"
if [ -d "$INSTALL_DIR" ] && [ "$(ls -A "$INSTALL_DIR" 2>/dev/null)" ]; then
  warn "Harness folder already exists: $INSTALL_DIR"
  if [ "${HARNESS_OVERWRITE:-}" = "1" ]; then
    detail "HARNESS_OVERWRITE=1 — continuing"
  else
    read -rp "$(echo -e "${CYAN}?${NC} Overwrite files in this folder? (y/N): ")" OVERWRITE
    if [[ ! "$OVERWRITE" =~ ^[Yy]$ ]]; then
      echo "Exiting. Choose a different path (HARNESS_SUBDIR) or set HARNESS_OVERWRITE=1."
      exit 1
    fi
  fi
else
  ok "Install location is clear"
fi

# --- Step 3/8 — Capture the project goal ---------------------------------------
step "Step 3/8 — Project goal"
PROJECT_GOAL="${HARNESS_PROJECT_GOAL:-}"
if [ -z "$PROJECT_GOAL" ]; then
  echo -e "Describe in one line what you want to build or change in ${BOLD}$APP_NAME${NC}."
  read -rp "$(echo -e "${CYAN}?${NC} Project goal: ")" PROJECT_GOAL
fi
if [ -z "${PROJECT_GOAL// /}" ]; then
  echo -e "${YELLOW}✗${NC} No goal provided. The /plan handoff needs a goal. Exiting."
  exit 1
fi
detail "Goal: $PROJECT_GOAL"

# --- Step 4/8 — Lay down the harness tree (delegate to 01) ---------------------
step "Step 4/8 — Installing harness files"
DELEGATE_ARGS=()
[ "$WITH_ORCHESTRATOR" -eq 1 ] && DELEGATE_ARGS+=(--with-orchestrator)
HARNESS_PROJECT_PATH="$INSTALL_DIR" HARNESS_OVERWRITE=1 \
  "$DELEGATE" ${DELEGATE_ARGS[@]+"${DELEGATE_ARGS[@]}"}

# --- Step 5/8 — Re-title CLAUDE.md to the app name -----------------------------
step "Step 5/8 — Setting project identity"
python3 - "$INSTALL_DIR/CLAUDE.md" "$APP_NAME" <<'PY'
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
detail "CLAUDE.md title set to: $APP_NAME"
ok "Project identity set"

# --- Step 6/8 — Generate the deployment overlay (project-notes.md) -------------
step "Step 6/8 — Wiring the harness to orchestrate $APP_NAME"

REPO_URL="$(git -C "$TARGET" remote get-url origin 2>/dev/null || true)"
[ -z "$REPO_URL" ] && REPO_URL="$TARGET"

# Detect the app's verify command from common manifests.
VERIFY_CMD=""
if   [ -f "$TARGET/package.json" ];      then VERIFY_CMD="npm test"
elif [ -f "$TARGET/pyproject.toml" ];    then VERIFY_CMD="pytest"
elif [ -f "$TARGET/requirements.txt" ];  then VERIFY_CMD="pytest"
elif [ -f "$TARGET/go.mod" ];            then VERIFY_CMD="go test ./..."
elif [ -f "$TARGET/Cargo.toml" ];        then VERIFY_CMD="cargo test"
fi
if [ -n "$VERIFY_CMD" ]; then
  detail "Detected stack verify command: $VERIFY_CMD"
else
  detail "No known stack detected — verify hints left as comments"
fi

TEMPLATE_OVERLAY="$INSTALL_DIR/_config/project-notes.TEMPLATE.md"
OUT_OVERLAY="$INSTALL_DIR/_config/project-notes.md"
python3 - "$TEMPLATE_OVERLAY" "$OUT_OVERLAY" "$APP_NAME" "$REPO_URL" "$VERIFY_CMD" <<'PY'
from pathlib import Path
import sys

tmpl, out, name, repo, verify = sys.argv[1:6]
src = Path(tmpl)
if not src.exists():
    # Minimal overlay if the template was trimmed.
    text = "# Project Notes (deployment overlay)\n"
else:
    text = src.read_text()

# Fill the Project block placeholders.
text = text.replace("**Name:** `<your-project-name>`", f"**Name:** `{name}`")
text = text.replace(
    "**Repo:** `<GitHub/GitLab URL or local path>`",
    f"**Repo:** `{repo}`",
)

# Anchor the harness to the app it orchestrates: the app root is one level up
# from this subfolder install. Skills read this overlay to act on the app.
anchor = (
    "**Repo:** `" + repo + "`\n"
    "**App root (orchestrated app):** `..` "
    "(this harness lives in a subfolder of the app it develops)"
)
text = text.replace(f"**Repo:** `{repo}`", anchor, 1)

# Insert the detected verify command into the "Verify green" block.
if verify:
    marker = "# Project-specific tests - uncomment and customize:"
    if marker in text:
        text = text.replace(
            marker,
            marker + "\n" + verify + "    # detected from app manifest",
            1,
        )

Path(out).write_text(text)
PY
detail "Wrote: $SUBDIR/_config/project-notes.md (Name, Repo, App root: .., verify hint)"
ok "Deployment overlay generated"

# --- Step 7/8 — Seed the initial task + handoff marker -------------------------
step "Step 7/8 — Seeding the initial task for /plan"

SEED_REL="stages/01-task-definition/INITIAL.md"
SEED_PATH="$INSTALL_DIR/$SEED_REL"
mkdir -p "$(dirname "$SEED_PATH")"
cat > "$SEED_PATH" <<EOF
# Task: $PROJECT_GOAL

## Goal

$PROJECT_GOAL

## Context

This harness is installed in a subfolder (\`$SUBDIR/\`) of the application it
develops. The application under development lives at the harness's parent
directory: \`..\` (relative to this harness root, i.e. \`$SUBDIR/\`).

- **App:** $APP_NAME
- **App root:** \`..\`
- **Repo:** $REPO_URL

Before planning, read \`_config/project-notes.md\` for the app's verify commands,
resume pointers, and any deployment-specific constraints. All implementation
work targets the application at \`..\`, not the harness itself.

## Success Criteria

- The goal above is delivered in the application at \`..\`.
- Changes verify green using the app's test command (see \`_config/project-notes.md\`).
- Plan, build, and review follow the harness lifecycle (\`CONTEXT.md\`).

## Task for Planner Agent

Create an implementation-ready plan for the goal above:

1. Read \`_config/project-notes.md\` and explore the app at \`..\` for relevant patterns.
2. Define scope, assumptions, affected files (under \`..\`), and validation criteria.
3. Write the plan to \`plans/<plan-name>.md\` (see \`plans/README.md\`).
4. Recommend the next agent (Reviewer, then Builder) before any commit.
EOF
detail "Wrote: $SUBDIR/$SEED_REL"

HANDOFF_PATH="$INSTALL_DIR/.harness-handoff"
cat > "$HANDOFF_PATH" <<EOF
# Harness handoff marker — consumed by the 'new-project' skill.
# Next action (path relative to harness root):
plan $SEED_REL
EOF
detail "Wrote: $SUBDIR/.harness-handoff"
ok "Initial task seeded and handoff marker written"

# --- Step 8/8 — Validate + summary ---------------------------------------------
step "Step 8/8 — Validating installed harness"
VALIDATOR="$INSTALL_DIR/scripts/07-validate-harness.sh"
VALIDATION_SUMMARY="(validation script not found)"
if [ -x "$VALIDATOR" ]; then
  VALIDATION_OUTPUT="$(PROJECT_ROOT="$INSTALL_DIR" "$VALIDATOR" 2>&1 || true)"
  VALIDATION_SUMMARY="$(echo "$VALIDATION_OUTPUT" | grep -E '^(Passed|Warnings|Failed):' | tr -s ' ' | paste -sd '·' - | sed 's/·/  ·  /g')"
  [ -z "$VALIDATION_SUMMARY" ] && VALIDATION_SUMMARY="$(echo "$VALIDATION_OUTPUT" | tail -n 1)"
  ok "Validator ran"
else
  warn "Validator not found at $VALIDATOR"
fi

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   ✅  Harness installed and ready to orchestrate ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${BOLD}App:${NC}        $APP_NAME"
echo -e "  ${BOLD}Harness:${NC}    $INSTALL_DIR"
echo -e "  ${BOLD}Goal:${NC}       $PROJECT_GOAL"
echo -e "  ${BOLD}Validation:${NC} $VALIDATION_SUMMARY"
if [ "$WITH_ORCHESTRATOR" -eq 1 ]; then
  echo -e "  ${BOLD}Orchestrator:${NC} included (python3 $SUBDIR/scripts/orchestrate.py --help)"
fi
echo ""
echo -e "  ${CYAN}Next step — start development with the PLAN process:${NC}"
echo -e "  The ${BOLD}new-project${NC} skill auto-continues into /plan using the seeded task."
echo -e "  To run it yourself, from the harness root (${BOLD}$SUBDIR/${NC}):"
echo ""
echo -e "      ${BOLD}/plan $SEED_REL${NC}"
echo ""
echo -e "  ${DIM}Point your AI assistant at $SUBDIR/CLAUDE.md to operate the harness.${NC}"
echo ""
