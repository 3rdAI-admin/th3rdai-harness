#!/usr/bin/env bash
# Maintainer checklist before tagging a harness template release.
# Runs structural validation, orchestrator tests, and a dry-run bootstrap.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="${TMPDIR:-/tmp}/harness-release-check-$$"
FAIL=0

GREEN='\033[0;32m'; RED='\033[0;31m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

step() { echo -e "\n${CYAN}━━━${NC} ${BOLD}$1${NC}"; }
ok()   { echo -e "${GREEN}✔${NC}  $1"; }
bad()  { echo -e "${RED}✗${NC}  $1"; FAIL=1; }

cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT

echo ""
echo -e "${BOLD}Harness template release checklist${NC}"
echo "Root: $ROOT"
echo ""

step "1/3 — Structural validation"
if PROJECT_ROOT="$ROOT" "$ROOT/scripts/07-validate-harness.sh"; then
  ok "07-validate-harness.sh passed"
else
  bad "07-validate-harness.sh failed"
fi

step "2/3 — Orchestrator unit tests"
if [ -d "$ROOT/scripts/orchestrator/tests" ]; then
  if (cd "$ROOT" && python3 -m unittest discover scripts/orchestrator/tests -q); then
    ok "Orchestrator tests passed"
  else
    bad "Orchestrator tests failed"
  fi
else
  echo "   (skipped — no scripts/orchestrator/tests/)"
fi

step "3/3 — Dry-run bootstrap (with orchestrator)"
mkdir -p "$TMP"
if HARNESS_PROJECT_PATH="$TMP/bootstrap-out" HARNESS_OVERWRITE=1 \
  "$ROOT/scripts/01-create-project.sh" --with-orchestrator >/dev/null 2>&1; then
  if PROJECT_ROOT="$TMP/bootstrap-out" "$TMP/bootstrap-out/scripts/07-validate-harness.sh" >/dev/null 2>&1; then
    ok "Bootstrap + validation passed"
  else
    bad "Bootstrapped project failed validation"
    PROJECT_ROOT="$TMP/bootstrap-out" "$TMP/bootstrap-out/scripts/07-validate-harness.sh" || true
  fi
else
  bad "Bootstrap script failed"
fi

echo ""
if [ "$FAIL" -eq 0 ]; then
  echo -e "${GREEN}${BOLD}Ready for template release.${NC}"
  echo ""
  echo "Next steps:"
  echo "  1. GitHub → Settings → General → enable Template repository"
  echo "  2. git tag -a v1.0.0 -m \"Harness template v1.0.0\""
  echo "  3. git push origin v1.0.0"
  echo "  4. Publish GitHub Release with link to DISTRIBUTION.md"
  exit 0
else
  echo -e "${RED}${BOLD}Release checklist failed — fix issues above before tagging.${NC}"
  exit 1
fi
