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

for dir in agents skills prompts models configs evals stages runs telemetry scripts shared _config plans; do
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
check_file "evals/rubrics/orchestrator-output-quality.md"
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
echo "Cross-reference checks"

# Agent contract and default_skill paths in configs/agents.yaml must resolve.
# This catches config drift such as a renamed skill file (e.g. plan.md -> planner.md).
agent_refs=$(grep -oE '(contract|default_skill):[[:space:]]*[^[:space:]]+' "$ROOT/configs/agents.yaml" 2>/dev/null | awk '{print $2}' | grep -v '^null$' || true)
if [ -n "$agent_refs" ]; then
  while IFS= read -r ref; do
    [ -z "$ref" ] && continue
    check_file "$ref"
  done <<< "$agent_refs"
else
  warn "configs/agents.yaml has no resolvable contract/default_skill paths"
fi

# Every agent referenced in configs/routing.yaml must have a contract file.
routing_agents=$(grep -oE '^[[:space:]]*-[[:space:]]+[a-z_]+' "$ROOT/configs/routing.yaml" 2>/dev/null | awk '{print $2}' | sort -u || true)
if [ -n "$routing_agents" ]; then
  while IFS= read -r agent; do
    [ -z "$agent" ] && continue
    if [ -f "$ROOT/agents/$agent.agent.md" ]; then
      ok "routing.yaml agent '$agent' has a contract"
    else
      fail "routing.yaml references agent '$agent' but agents/$agent.agent.md is missing"
    fi
  done <<< "$routing_agents"
fi

# Every model_profile referenced in configs/agents.yaml must exist in configs/models.yaml.
profile_refs=$(grep -oE 'model_profile:[[:space:]]*[^[:space:]]+' "$ROOT/configs/agents.yaml" 2>/dev/null | awk '{print $2}' | grep -v '^null$' | sort -u || true)
if [ -n "$profile_refs" ]; then
  while IFS= read -r profile; do
    [ -z "$profile" ] && continue
    if grep -qE "^[[:space:]]+$profile:" "$ROOT/configs/models.yaml"; then
      ok "model profile '$profile' is defined in models.yaml"
    else
      fail "agents.yaml references model profile '$profile' but it is missing from models.yaml"
    fi
  done <<< "$profile_refs"
fi

# Versioned prompt paths listed in prompts/registry.md must resolve.
prompt_refs=$(grep -oE '`[a-z0-9_-]+/v[0-9]+\.md`' "$ROOT/prompts/registry.md" 2>/dev/null | tr -d '`' || true)
if [ -n "$prompt_refs" ]; then
  while IFS= read -r ref; do
    [ -z "$ref" ] && continue
    check_file "prompts/$ref"
  done <<< "$prompt_refs"
fi

echo ""
echo "Stage contract coherence"

# Stage CONTEXT.md titles must match the renamed lifecycle purpose.
# This catches the failure mode where a stage dir was renamed but its
# contract still describes the old content workflow (Research/Draft/Review).
check_stage_title() {
  local f="stages/$1/CONTEXT.md"
  if [ -f "$ROOT/$f" ] && head -5 "$ROOT/$f" | grep -q "$2"; then
    ok "$f declares '$2'"
  else
    fail "$f missing expected title '$2' (stale or mislabeled contract)"
  fi
}
check_stage_title "01-task-definition" "Task Definition"
check_stage_title "02-agent-design" "Agent Design"
check_stage_title "03-prompt-design" "Prompt Design"
check_stage_title "04-tool-integration" "Tool Integration"
check_stage_title "05-evaluation" "Evaluation"
check_stage_title "06-iteration" "Iteration"
check_stage_title "07-release" "Release"

if grep -rqE "Stage 0[123]: (Research|Draft|Review)" "$ROOT/stages" 2>/dev/null; then
  fail "stale stage titles (Research/Draft/Review) found in stages/ contracts"
else
  ok "no stale Research/Draft/Review stage titles in stages/"
fi

# Model profiles should be filled in. Warn (do not fail): the harness is
# model-agnostic, but TBD values mean model routing is not yet usable.
if grep -qE '(provider|model):[[:space:]]*TBD' "$ROOT/configs/models.yaml" 2>/dev/null; then
  warn "configs/models.yaml has unfilled (TBD) provider/model values"
else
  ok "configs/models.yaml model profiles are filled in"
fi

echo ""
echo "Skill reference checks"

# Backtick-quoted repo file paths inside skill files should resolve.
# This is a WARN (not a fail): skill bodies legitimately reference forward-looking
# paths such as new prompt versions in usage examples. Hard wiring (agent contracts,
# default_skill, routing, model profiles, registry) is fail-checked above.
# Skipped automatically: placeholders (the char class stops at < > * ), "..." paths,
# and runtime-generated stage outputs (*/output/*).
skill_refs=$(grep -rhoE '`(agents|skills|prompts|configs|evals|stages|runs|telemetry|models|scripts|shared|_config|plans)/[A-Za-z0-9_./-]+\.(md|sh|ya?ml|py)`' "$ROOT/skills" 2>/dev/null | tr -d '`' | grep -v '\.\.\.' | grep -v '/output/' | sort -u || true)
if [ -n "$skill_refs" ]; then
  skill_ref_missing=0
  while IFS= read -r ref; do
    [ -z "$ref" ] && continue
    if [ ! -f "$ROOT/$ref" ]; then
      warn "skill files reference '$ref' (not found — example/forward path or typo?)"
      skill_ref_missing=1
    fi
  done <<< "$skill_refs"
  [ "$skill_ref_missing" -eq 0 ] && ok "all concrete file paths referenced in skills/ resolve"
fi

echo ""
echo "Eval case / rubric coherence"

# Every eval case must reference at least one rubric, and each referenced rubric
# file must exist. This wires the eval layer (cases + rubrics) into the gate so a
# case can't point at a missing or renamed rubric (e.g. orchestrator-output-quality).
shopt -s nullglob
eval_case_found=0
for case_path in "$ROOT"/evals/cases/*/*.md; do
  eval_case_found=1
  rel=${case_path#"$ROOT/"}
  refs=$(grep -oE 'evals/rubrics/[A-Za-z0-9._-]+\.md' "$case_path" 2>/dev/null | sort -u || true)
  if [ -z "$refs" ]; then
    fail "eval case '$rel' references no rubric"
    continue
  fi
  case_ok=1
  while IFS= read -r ref; do
    [ -z "$ref" ] && continue
    if [ ! -f "$ROOT/$ref" ]; then
      fail "eval case '$rel' references missing rubric '$ref'"
      case_ok=0
    fi
  done <<< "$refs"
  [ "$case_ok" -eq 1 ] && ok "eval case '$rel' -> rubric(s) resolve"
done
shopt -u nullglob
[ "$eval_case_found" -eq 0 ] && warn "no eval cases found under evals/cases/"

echo ""
echo "ICM pedagogical enhancements (optional)"

# New documentation from ICM integration - warnings only (backward compatible)
if [ -f "$ROOT/_config/conventions.md" ]; then
  ok "_config/conventions.md exists"
else
  warn "_config/conventions.md not found (optional ICM enhancement)"
fi

if [ -d "$ROOT/docs" ]; then
  ok "docs/ directory exists"
  if [ -f "$ROOT/docs/QUICK-REFERENCE.md" ]; then
    ok "docs/QUICK-REFERENCE.md exists"
  else
    warn "docs/QUICK-REFERENCE.md not found (optional ICM enhancement)"
  fi
else
  warn "docs/ directory not found (optional ICM enhancement)"
fi

# Check if stage CONTEXT.md files have token budget sections
token_budget_found=0
for stage in 01-task-definition 02-agent-design 03-prompt-design 04-tool-integration 05-evaluation 06-iteration 07-release; do
  if [ -f "$ROOT/stages/$stage/CONTEXT.md" ]; then
    if grep -q "## Token Budget" "$ROOT/stages/$stage/CONTEXT.md"; then
      token_budget_found=$((token_budget_found + 1))
    fi
  fi
done

if [ "$token_budget_found" -eq 7 ]; then
  ok "all stage CONTEXT.md files have token budget sections"
elif [ "$token_budget_found" -gt 0 ]; then
  warn "$token_budget_found/7 stage CONTEXT.md files have token budgets (partial adoption)"
else
  warn "no stage CONTEXT.md files have token budgets (optional ICM enhancement)"
fi

echo ""
echo "Passed:   $PASS"
echo "Warnings: $WARN"
echo "Failed:   $FAIL"

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
