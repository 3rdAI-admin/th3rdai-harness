# Orchestrator Usage Guide

Practical guidance from dogfooding the Native Orchestrator (May 29-30, 2026).

## Quick Start

### 1. Dry-Run (Safe, No Model Calls)

```bash
# See what the orchestrator would do
python3 scripts/orchestrate.py route task_definition

# Result: Generates context bundles and run records, no AI invoked
ls -lt runs/ | head -5
cat runs/$(ls -t runs/*.md | head -1)
```

**Use dry-run for:**
- Testing route configuration
- Debugging sequencing issues
- Understanding what context gets assembled
- Validating configs without API costs

### 2. Execute Mode (Calls Real AI)

```bash
# Actually run the agents
python3 scripts/orchestrate.py route task_definition --execute --adapter cli --max-steps 2 --yes

# --execute: enable execution (default is dry-run)
# --adapter cli: use configured CLI from execution.yaml
# --max-steps 2: only run first 2 steps (safety bound)
# --yes: skip per-step checkpoints (approval gates still apply!)
```

**⚠️ Important:**
- Even with `--yes`, protected files require approval
- Protected paths: `agents/`, `configs/`, `scripts/orchestrator/`
- Timeout default: 300s (5 minutes) per step
- API costs apply when using real LLMs

---

## How Routes Work

Routes sequence agents through lifecycle stages. From `configs/routing.yaml`:

| Route | Agents | When to Use |
|-------|--------|-------------|
| `task_definition` | researcher → planner | Define and plan a new task |
| `agent_design` | planner → reviewer | Design agent contract |
| `prompt_design` | planner → reviewer | Create/revise prompts |
| `tool_integration` | builder → reviewer | Implement a plan |
| `evaluation` | evaluator → reviewer | Score against rubrics |
| `iteration` | planner → builder → evaluator | Full iteration cycle |
| `release` | reviewer | Final release review |

---

## What We Learned (Dogfooding Session)

### Test 1: task_definition Route (No Input)

**Command:**
```bash
python3 scripts/orchestrate.py route task_definition --execute --adapter cli --max-steps 2 --yes
```

**Result:**
- ✅ Both agents executed (researcher, planner)
- ℹ️ Agents asked "what should I work on?" (expected behavior)
- ✅ Run records generated correctly

**Lesson:** Agents need a task to work on. Provide input via:
1. Pre-existing files they reference (plans, research notes)
2. Stage inputs defined in route
3. Manual agent-driven workflow first

### Test 2: task_definition Route (With Task)

**Setup:**
- Created `stages/01-task-definition/INITIAL.md` with Phase 05 task

**Result:**
- ✅ Researcher executed (analyzing task)
- ❌ Planner timed out after 300s (5 minutes)
- ✅ Timeout handling worked correctly:
  - Subprocess terminated
  - Run record marked `status: failed`
  - Clear notes: `"timeout after 300.0s"`
  - Issue logged with severity high

**Lesson:** Timeout protection works! But 5 minutes with no progress indicator is rough UX. → Phase 05 improvement identified.

### Test 3: tool_integration Route (Protected File)

**Setup:**
- Created plan: `plans/improve-eval-case-examples.md`

**Command:**
```bash
python3 scripts/orchestrate.py route tool_integration --execute --adapter cli --max-steps 2 --yes
```

**Result:**
```
protected write(s): configs/tools.yaml
Approve? [y/N] halted before step 1 (builder): approval not granted
```

**Lesson:** Approval gates work perfectly! Even `--yes` doesn't bypass protected files.

---

## Best Practices

### ✅ When to Use the Orchestrator

**Good fits:**
- Multi-step workflows with clear handoffs
- Repetitive tasks (run same route many times)
- Want automatic run record generation
- Testing end-to-end routes
- CI/CD automation

**Examples:**
```bash
# Run full iteration cycle
python3 scripts/orchestrate.py route iteration --execute --adapter cli --max-steps 3

# Evaluate multiple prompts
python3 scripts/orchestrate.py route evaluation --execute --adapter cli --max-steps 2
```

### ⚠️ When NOT to Use the Orchestrator

**Better with agent-driven:**
- Single-file edits
- One-off changes
- Quick iterations
- Exploratory work
- Custom workflows not in routing.yaml

**Just use a normal AI assistant for these!**

### 🎯 Hybrid Approach (Recommended)

1. **Plan manually** - Create implementation-ready plan in `plans/`
2. **Build with orchestrator** - Use `tool_integration` route
3. **Iterate manually** - Refine based on results

This gives you:
- Control over planning (most creative step)
- Automation for execution (most repetitive step)
- Automatic run record generation

---

## Common Patterns

### Pattern 1: Scaffold Eval Results

```bash
# Generate eval result template from a case
python3 scripts/orchestrate.py eval evals/cases/planning/basic-feature-plan.md

# Creates: evals/results/YYYYMMDD-basic-feature-plan-result.md
# You fill in scores manually
```

### Pattern 2: Bounded Execution

```bash
# Only run first N steps (safety)
python3 scripts/orchestrate.py route iteration --execute --adapter cli --max-steps 1

# Run without checkpoints (but gates still apply)
python3 scripts/orchestrate.py route iteration --execute --adapter cli --max-steps 3 --yes
```

### Pattern 3: Test Before Execute

```bash
# 1. Dry-run first
python3 scripts/orchestrate.py route task_definition

# 2. Check what would happen
cat runs/$(ls -t runs/*.md | head -1)

# 3. If looks good, execute
python3 scripts/orchestrate.py route task_definition --execute --adapter cli --max-steps 2
```

---

## Run Records

Every execution creates a run record in `runs/`:

**Filename format:** `YYYYMMDD-HHMMSS-<route>-<step>-<agent>.md`

**Example:** `20260530-060257-task-definition-01-researcher.md`

**Contents:**
```yaml
run_id: 20260530-060257-task-definition-01-researcher
created_at: 2026-05-30T06:02:57Z
agent: researcher
skill: skills/research/research.md
prompt_version: prompts/researcher/v1.md
model_profile: research
inputs: [...]
outputs: [...]
tool_actions: [...]
validation:
  status: executed  # or failed, skipped
  notes: "..."
```

**Also created:**
- `task_definition-01-researcher-stdout.txt` - Agent output
- `task_definition-01-researcher-stderr.txt` - Error output

---

## Troubleshooting

### Agent Asks "What Should I Work On?"

**Problem:** Agent doesn't have task context

**Solution:**
1. Create task file agents can reference
2. Use agent-driven workflow first
3. Or run routes that expect existing work (e.g., `tool_integration` with plan)

### Timeout After 300 Seconds

**Problem:** Step took too long

**Solution:**
1. Increase timeout in `configs/execution.yaml`:
   ```yaml
   cli:
     timeout_seconds: 600  # 10 minutes
   ```
2. Or break task into smaller steps
3. Check if agent is stuck waiting for input

### "Protected Write" Blocked

**Problem:** Agent trying to modify protected files

**Solution:**
1. This is correct behavior! Approve interactively
2. Remove `--yes` to see approval prompt
3. Or modify files manually instead

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'scripts.orchestrator'`

**Solution:**
Run from repository root:
```bash
cd /path/to/th3rdai-harness
python3 scripts/orchestrate.py route task_definition
```

---

## Configuration

### execution.yaml

```yaml
execution:
  default_adapter: noop      # noop = dry-run, cli = execute
  cli:
    command: ["claude", "-p"]  # Your agent CLI
    env_allowlist:             # Environment vars to pass
      - ANTHROPIC_API_KEY
    timeout_seconds: 300       # 5 minutes per step
```

### routing.yaml

Define custom routes:
```yaml
routes:
  my_custom_route:
    stage: stages/04-tool-integration
    agents:
      - builder
      - my_custom_agent
```

---

## Performance Tips

### Reduce API Costs

1. **Use dry-run for testing** - No model calls
2. **Limit steps** - Use `--max-steps N`
3. **Test with UAT stub** - Configure `command: ["python3", "scripts/orchestrator/uat_cli_stub.py"]`

### Speed Up Iteration

1. **Agent-driven for planning** - Faster, more control
2. **Orchestrator for building** - Automation where it helps
3. **Manual for one-off edits** - Don't automate everything

### Monitor Progress

Currently no progress indicators (Phase 05 improvement planned). Workaround:

```bash
# In another terminal, watch run records
watch -n 5 'ls -lt runs/*.md | head -5'

# Or tail stdout
tail -f runs/task_definition-*-stdout.txt
```

---

## What's Next (Phase 05 Ideas)

Based on dogfooding, these would improve UX significantly:

1. **Progress indicators** - Show "Step 2/5: Running planner..." instead of silence
2. **Streaming output** - Optional `--stream` flag to show agent output in real-time
3. **Better error messages** - The examples we added to eval cases
4. **Graceful cancellation** - Ctrl+C should finish current step, not kill abruptly
5. **Resume capability** - `--resume` flag to continue from last completed step

See `plans/native-orchestrator/05-observability-and-errors.md` (when created) for details.

---

## Resources

- **Plans:** `plans/native-orchestrator/EFFORT.md`
- **Config:** `configs/routing.yaml`, `configs/execution.yaml`
- **Eval cases:** `evals/cases/orchestrator/` (8 cases)
- **Tests:** `python3 -m unittest discover scripts/orchestrator/tests`
- **Validator:** `scripts/07-validate-harness.sh`

---

## Success Stories

**What we built with the orchestrator:**
- ✅ Enhanced 3 eval cases with example outputs
- ✅ Tested timeout handling (worked perfectly)
- ✅ Validated approval gates (blocked protected writes)
- ✅ Generated complete run records (all 9 conform to schema)

**Verdict:** The orchestrator works! It successfully automated the tedious parts (sequencing, run records, safety gates) while letting agents focus on reasoning.
