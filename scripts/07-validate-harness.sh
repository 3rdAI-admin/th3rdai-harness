#!/usr/bin/env bash
set -euo pipefail

ROOT="${PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
PASS=0
FAIL=0
WARN=0

ok() { printf '✔ %s\n' "$1"; PASS=$((PASS + 1)); }
fail() { printf '✗ %s\n' "$1"; FAIL=$((FAIL + 1)); }
warn() { printf '⚠ %s\n' "$1"; WARN=$((WARN + 1)); }

check_file() {
  if [ -f "$ROOT/$1" ]; then
    ok "$1 exists"
  else
    fail "$1 is missing"
  fi
}

check_dir() {
  if [ -d "$ROOT/$1" ]; then
    ok "$1/ exists"
  else
    fail "$1/ is missing"
  fi
}

echo "AI Agent Development Harness validation"
echo "Root: $ROOT"
echo ""

check_file "CLAUDE.md"
check_file "CONTEXT.md"
check_file "FRAMEWORK.md"
check_file "README.md"

for dir in agents skills prompts models configs evals stages runs telemetry scripts shared _config; do
  check_dir "$dir"
done

for agent in researcher planner builder reviewer evaluator; do
  check_file "agents/$agent.agent.md"
done

for cfg in agents models routing tools; do
  check_file "configs/$cfg.yaml"
done

for stage in \
  01-task-definition \
  02-agent-design \
  03-prompt-design \
  04-tool-integration \
  05-evaluation \
  06-iteration \
  07-release; do
  check_dir "stages/$stage"
  check_file "stages/$stage/CONTEXT.md"
done

check_file "prompts/registry.md"
check_file "evals/README.md"
check_file "evals/rubrics/plan-quality.md"
check_file "evals/rubrics/tool-safety.md"
check_file "evals/rubrics/agent-output-quality.md"
check_file "telemetry/run-log-schema.md"

if grep -q "stages/01-task-definition" "$ROOT/CONTEXT.md"; then
  ok "CONTEXT.md routes to agent lifecycle stages"
else
  fail "CONTEXT.md does not route to agent lifecycle stages"
fi

if grep -q "agents/" "$ROOT/FRAMEWORK.md" && grep -q "evals/" "$ROOT/FRAMEWORK.md"; then
  ok "FRAMEWORK.md documents agent and eval layers"
else
  warn "FRAMEWORK.md may be missing core layer documentation"
fi

echo ""
echo "Passed:   $PASS"
echo "Warnings: $WARN"
echo "Failed:   $FAIL"

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
