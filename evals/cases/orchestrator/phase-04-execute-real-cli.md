# Eval Case: Phase 04 Execute with Real Agent CLI

## Purpose

Validate that Phase 04 execution adapter works end-to-end with a real agent CLI
(e.g., `claude -p`, `aider`, or similar). This goes beyond the UAT stub to verify
actual model invocation, approval gates, environment scrubbing, and run record
capture with real agent output.

## Prerequisites

- `configs/execution.yaml` configured with a real agent CLI command
- CLI command must accept stdin prompt and produce stdout output
- API key configured in environment if required (e.g., ANTHROPIC_API_KEY for Claude)
- `configs/execution.yaml` `cli.env_allowlist` includes necessary API key env vars

## Input

Execute a simple route with real CLI:

```bash
# Verify execution.yaml is configured
cat configs/execution.yaml
# Should show real CLI command, e.g.:
# cli:
#   command: ["claude", "-p"]
#   env_allowlist: ["ANTHROPIC_API_KEY"]
#   timeout_seconds: 120

# Run single-step execution
python3 scripts/orchestrate.py route task_definition --execute --adapter cli --max-steps 1
```

## Expected Behavior

The orchestrator should:

1. **Assemble context bundle** (contract + skill + prompt + inputs)
2. **Invoke configured CLI** with bundle on stdin
3. **Capture stdout/stderr** to files under `runs/`
4. **Scrub environment** (only PATH/HOME/LANG/USER + allowed API keys)
5. **Enforce timeout** (default 120s, configurable)
6. **Apply approval gates** from `configs/tools.yaml`
   - Per-step checkpoint (unless `--yes` provided)
   - Per-action gates (git commit, npm install, etc.) never bypassed by `--yes`
7. **Write complete run record** with:
   - `status: executed` (or `failed` if CLI exits non-zero)
   - `outputs: [...]` (files created by agent)
   - `tool_actions: [...]` (actions agent attempted)
   - `stdout_path` and `stderr_path` (captured output files)
   - `exit_code` from subprocess
8. **Respect `--max-steps`** bound (stop after N steps)

## Test Execution

```bash
# Full execution with checkpoints (interactive)
python3 scripts/orchestrate.py route task_definition --execute --adapter cli --max-steps 2

# Unattended with approval bypass (gates still apply)
python3 scripts/orchestrate.py route task_definition --execute --adapter cli --max-steps 1 --yes

# Verify run record was created
ls -lt runs/ | head -5

# Check run record contents
LATEST_RUN=$(ls -t runs/*.md | head -1)
cat "$LATEST_RUN"

# Verify stdout captured
cat runs/*-stdout.txt

# Verify stderr captured (may be empty)
cat runs/*-stderr.txt 2>/dev/null || echo "No stderr"
```

## Expected Run Record Structure

```yaml
run_id: 20260529-123456-task-definition-01-researcher
created_at: "2026-05-29T12:34:56Z"
request:
  type: execute_route
  route: task_definition
  step: 1
  max_steps: 2
agent:
  name: researcher
  contract: agents/researcher.md
  skill: skills/research/research.md
  prompt: prompts/research/v1.md
  model_profile: models/profiles/sonnet-research.md
inputs:
  - stages/01-task-definition/README.md
  - shared/context.md
execution:
  adapter: cli
  command: ["claude", "-p"]
  timeout_seconds: 120
  exit_code: 0
  stdout_path: runs/20260529-123456-task-definition-01-researcher-stdout.txt
  stderr_path: runs/20260529-123456-task-definition-01-researcher-stderr.txt
outputs:
  - stages/01-task-definition/outputs/research-notes.md  # example
tool_actions:
  - "git status"
  - "read FRAMEWORK.md"
  # (extracted from agent's stdout/execution trace)
validation:
  status: executed
  notes: "Agent completed successfully"
  rubric_used: null  # rubric evaluation happens separately
```

## Rubric

Use `evals/rubrics/orchestrator-output-quality.md`. Focus on:

- **Run-record schema conformance** (score 4+): All execution fields present and correct
- **Safety adherence** (score 4+): Environment scrubbed, approval gates enforced
- **Path correctness** (score 4+): All paths repo-root-relative
- **Failure transparency** (score 4+): Non-zero exit codes captured correctly
- **Reproducibility** (score 3+): Re-running produces equivalent behavior (modulo model nondeterminism)

## Pass Criteria

### Required (must pass all):
- Run record created with `status: executed` or `status: failed` (not `skipped`)
- stdout/stderr captured to files with correct paths
- Exit code captured in run record
- Environment was scrubbed (verify no unintended env vars leaked)
- Configured timeout is respected (subprocess terminated if exceeded)
- `--max-steps` bound is enforced (execution stops after N steps)

### Expected (should pass most):
- Agent produced meaningful output (not empty/error)
- Outputs list contains files created by agent
- Tool actions list contains commands agent attempted
- Approval gates triggered appropriately (if agent attempted gated actions)
- Run record validates against `telemetry/run-log-schema.md`

### Optional (nice to have):
- Agent completed task successfully
- Agent output passes relevant rubric evaluation
- No API rate limit errors
- CLI execution time reasonable (<60s for simple task)

## Safety Verification

After execution, verify:

```bash
# Environment was scrubbed (check no API key in stdout/stderr if not expected)
grep -i "api.key" runs/*-stdout.txt runs/*-stderr.txt && echo "WARNING: API key may have leaked" || echo "OK: No API key in output"

# Approval gates were enforced (if agent attempted gated action)
# Check run record shows action was blocked or approved
grep -A5 "tool_actions" "$LATEST_RUN"

# Subprocess didn't leak (no zombie processes)
ps aux | grep claude | grep -v grep || echo "OK: No orphaned CLI processes"
```

## Failure Modes to Test

1. **CLI not configured** - should fail with clear error
2. **CLI command invalid** - should fail with clear error
3. **API key missing** - should fail with auth error (captured in stderr)
4. **Timeout exceeded** - should terminate and mark failed with timeout note
5. **CLI exits non-zero** - should mark failed with exit code
6. **Gated action attempted** - should prompt for approval (or block if not approved)

## Notes

- This case validates the entire Phase 04 stack end-to-end
- Real model invocation means results will vary (use for validation, not regression testing)
- For regression tests, use deterministic stubs (like UAT stub)
- API costs may apply when running this case with real LLMs
- Recommended to run manually during milestone validation, not in CI/CD
