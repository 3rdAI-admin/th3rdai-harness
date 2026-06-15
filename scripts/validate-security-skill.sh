#!/usr/bin/env bash
# Validate portable harness/skills/security (no app-specific paths).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

fail() { printf '\n\033[31mFAIL:\033[0m %s\n' "$1"; exit 1; }
ok() { printf '\033[32m✔\033[0m %s\n' "$1"; }

echo "Portable security skill validation"
echo "Harness: $ROOT"
echo

for f in skills/security/SKILL.md skills/security/security.md; do
  [ -f "$f" ] || fail "missing $f"
  ok "$f exists"
done

grep -q 'skills/security/security.md' skills/security/SKILL.md \
  || fail "SKILL.md must reference skills/security/security.md"
ok "SKILL.md → security.md link"

# Portable skill must not reference VIRA-specific paths
if grep -qE 'vira/|VIRA_WASA|web_auth_token|frontend/src/webAuth' skills/security/security.md; then
  fail "skills/security/security.md contains VIRA-specific references"
fi
ok "security.md has no VIRA-specific paths"

refs=(
  agents/reviewer.agent.md
  evals/rubrics/agent-output-quality.md
  evals/rubrics/tool-safety.md
  evals/cases/code-review/security-bug-review.md
  configs/tools.yaml
  _config/security-baseline.TEMPLATE.md
)
for ref in "${refs[@]}"; do
  [ -e "$ref" ] || fail "harness ref missing: $ref"
done
ok "harness cross-references resolve (${#refs[@]} paths)"

if grep -q 'skills/security/security.md' evals/README.md; then
  ok "evals/README.md links security eval → portable skill"
else
  fail "evals/README.md missing portable skill link"
fi

if bash scripts/07-validate-harness.sh >/tmp/harness-validate.out 2>&1; then
  ok "07-validate-harness.sh passed"
else
  cat /tmp/harness-validate.out
  fail "07-validate-harness.sh failed"
fi

printf '\n\033[32m✓ portable security skill validation passed\033[0m\n'
