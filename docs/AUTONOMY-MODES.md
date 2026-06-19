# Autonomy Modes

**Version:** 1.2.0
**Status:** Production-ready
**Applies to:** Orchestrator execution (`scripts/orchestrate.py route --execute`)

## Overview

The AI Agent Development Harness supports **3 autonomy modes** that control approval behavior during orchestrator execution:

| Mode | Behavior | Use When |
|------|----------|----------|
| **Ask** | Approve all operations manually | Unfamiliar codebases, high-risk changes, learning mode |
| **Cautious** | Auto-approve LOW/MEDIUM, ask for HIGH, block CRITICAL | Most development work (recommended default) |
| **Full** | Auto-approve all operations | Trusted plans, comprehensive tests, time-sensitive deploys |

All autonomy decisions are logged to `runs/autonomy-decisions.jsonl` for audit and review.

## Quick Start

### Set Default Mode (Config)

Edit `configs/autonomy.yaml`:

```yaml
mode: cautious  # ask | cautious | full
```

### Override Mode (CLI)

```bash
# Ask mode - approve everything manually
python3 scripts/orchestrate.py route iteration --execute --adapter cli --autonomy ask

# Cautious mode - balanced autonomy
python3 scripts/orchestrate.py route iteration --execute --adapter cli --autonomy cautious

# Full mode - maximum autonomy
python3 scripts/orchestrate.py route release --execute --adapter cli --autonomy full --yes
```

CLI flag always overrides config default.

## Risk Levels

Operations are classified into 4 risk levels:

| Risk | Caller Count | Examples | Ask | Cautious | Full |
|------|--------------|----------|-----|----------|------|
| **LOW** | 0-3 | Read files, git status, list directory, documentation | Ask | Auto | Auto |
| **MEDIUM** | 4-9 | Edit existing files, write new files, git commit, refactor with tests | Ask | Auto | Auto |
| **HIGH** | 10-24 | Delete files, git push, breaking API changes, large refactors | Ask | Ask | Auto |
| **CRITICAL** | 25+ or critical path | Force push, production deploy, security boundaries, mass operations | Ask | **Block** | Auto |

### Risk Classification Rules

1. **Protected Writes** → HIGH risk
   - Files in `agents/`, `configs/`, `scripts/orchestrator/` (self-modification guard)

2. **Gated Actions** → HIGH risk
   - Commands matching `requires_approval` phrases in `configs/tools.yaml`

3. **GitNexus Impact** (when available)
   - 0-3 callers → LOW
   - 4-9 callers → MEDIUM
   - 10-24 callers → HIGH
   - 25+ callers OR critical process → CRITICAL

4. **Heuristic Fallback** (when GitNexus unavailable)
   - Pattern matching on operation descriptions
   - Conservative default: MEDIUM

## Mode Behavior

### Ask Mode

**Philosophy:** Maximum control, zero automation

```bash
python3 scripts/orchestrate.py route iteration --execute --adapter cli --autonomy ask
```

**Behavior:**
- ✅ Prompts for approval on **every step** regardless of risk level
- ✅ User types `y` or `yes` to proceed, anything else halts
- ✅ Audit log records `user_approved` or `user_rejected`

**Use when:**
- Operating in unfamiliar codebases
- Implementing high-risk changes
- Learning how the orchestrator works
- Maximum safety required

**Example output:**
```
Step 1 (planner @ stages/06-iteration) — risk: MEDIUM. Approve? [y/N] y
Step 2 (builder @ stages/06-iteration) — risk: MEDIUM. Approve? [y/N] y
```

### Cautious Mode (Default)

**Philosophy:** Autonomous for routine work, human oversight for risks

```bash
python3 scripts/orchestrate.py route iteration --execute --adapter cli --autonomy cautious
# Or omit --autonomy to use config default
```

**Behavior:**
- ✅ **AUTO-APPROVES** LOW risk (read, status, query, documentation)
- ✅ **AUTO-APPROVES** MEDIUM risk (edits, writes, commits, small refactors)
- ⚠️ **ASKS** for HIGH risk (deletes, push, breaking changes)
- 🛑 **BLOCKS** CRITICAL risk (force operations, 25+ callers, production deploys)

**Use when:**
- Most development and iteration work
- Orchestrating multi-step plans
- Batch operations with review checkpoints
- Balanced speed and safety

**Example output:**
```
Autonomy mode: cautious (Autonomous for low-risk, ask for high-risk, block critical)
✓ Step 1 (planner): MEDIUM risk auto-approved
✓ Step 2 (builder): MEDIUM risk auto-approved
Step 3 (builder @ stage/06-iteration) — risk: HIGH; gated: git push. Approve? [y/N]
```

### Full Mode

**Philosophy:** Maximum automation with comprehensive audit logging

```bash
python3 scripts/orchestrate.py route release --execute --adapter cli --autonomy full --yes
```

**Behavior:**
- ✅ **AUTO-APPROVES** all risk levels (LOW, MEDIUM, HIGH, CRITICAL)
- ✅ Comprehensive audit logging of every decision
- ✅ No prompts, no interruptions

**Use when:**
- Executing validated plans with complete test coverage
- Batch operations over trusted, well-tested code
- Time-sensitive deployments after manual review
- Automated CI/CD pipelines

**Example output:**
```
Autonomy mode: full (Full autonomy - make all decisions)
✓ Step 1 (reviewer): MEDIUM risk auto-approved
✓ Step 2 (builder): HIGH risk auto-approved
Autonomy summary: 2 auto-approved, 0 user-approved, 0 rejected, 0 blocked
```

## Audit Logging

### Log Location

`runs/autonomy-decisions.jsonl` (JSONL format - one JSON object per line)

### Log Format

```json
{
  "timestamp": "2026-06-19T11:42:56.968746",
  "mode": "cautious",
  "operation": "reviewer @ stages/07-release",
  "risk_level": "MEDIUM",
  "decision": "auto_approved",
  "context": {
    "step": 1,
    "agent": "reviewer",
    "stage": "stages/07-release",
    "outputs": ["output/release-notes.md", "runs/<run-id>.md"],
    "gated": [],
    "protected": []
  }
}
```

### Decision Types

| Decision | Meaning |
|----------|---------|
| `auto_approved` | Autonomy manager approved without user input |
| `user_approved` | User explicitly approved when prompted |
| `user_rejected` | User explicitly rejected when prompted |
| `blocked` | Autonomy manager blocked (CRITICAL in cautious mode) |

### Viewing Audit Logs

```bash
# View all decisions
cat runs/autonomy-decisions.jsonl | python3 -c "import sys, json; [print(json.dumps(json.loads(l), indent=2)) for l in sys.stdin]"

# View last 10 decisions
tail -10 runs/autonomy-decisions.jsonl

# Count by decision type
cat runs/autonomy-decisions.jsonl | python3 -c "import sys, json; from collections import Counter; entries = [json.loads(l) for l in sys.stdin]; counts = Counter(e['decision'] for e in entries); print(counts)"

# Filter by risk level
cat runs/autonomy-decisions.jsonl | python3 -c "import sys, json; [print(json.dumps(json.loads(l), indent=2)) for l in sys.stdin if json.loads(l)['risk_level'] == 'HIGH']"
```

## Configuration

### Config File: `configs/autonomy.yaml`

```yaml
# Default mode (used when --autonomy flag not provided)
mode: cautious

# Mode definitions
modes:
  ask:
    description: "Require explicit approval for all decisions"
    auto_approve_risk_levels: []

  cautious:
    description: "Autonomous for low-risk, ask for high-risk, block critical"
    auto_approve_risk_levels:
      - LOW
      - MEDIUM
    stop_on_risk_levels:
      - CRITICAL

  full:
    description: "Full autonomy - make all decisions"
    auto_approve_risk_levels:
      - LOW
      - MEDIUM
      - HIGH
      - CRITICAL

# Risk classifications
risk_classifications:
  file_operations:
    read: LOW
    edit_existing: LOW
    write_new: MEDIUM
    delete: HIGH

  git_operations:
    status: LOW
    commit: MEDIUM
    push: HIGH
    force_push: CRITICAL

  gitnexus_impact:
    0-3_callers: LOW
    4-9_callers: MEDIUM
    10-24_callers: HIGH
    25+_callers: CRITICAL
    critical_path: CRITICAL

# Audit log configuration
audit:
  enabled: true
  output_path: "runs/autonomy-decisions.jsonl"
  include_context: true

# Safety guardrails (hard blocks regardless of mode)
safety:
  always_block:
    - force_push_to_main
    - force_push_to_master
    - production_database_drop
```

### Customizing Risk Classifications

Edit `configs/autonomy.yaml` to adjust risk levels for your project:

```yaml
risk_classifications:
  # Add custom operation types
  api_operations:
    read: LOW
    create: MEDIUM
    update: MEDIUM
    delete: HIGH
    admin: CRITICAL

  # Adjust caller thresholds
  gitnexus_impact:
    0-5_callers: LOW      # Increase LOW threshold
    6-15_callers: MEDIUM  # Wider MEDIUM range
    16+_callers: HIGH     # Lower HIGH threshold
```

## Agent-Specific Guidance

### Builder Agent

**Recommended mode:** `--autonomy full` for trusted batch operations

```bash
# Example: Execute validated plan with full autonomy
python3 scripts/orchestrate.py route iteration --execute --adapter cli --autonomy full --yes
```

**Review audit log** after completion:
```bash
cat runs/autonomy-decisions.jsonl | tail -20
```

### Planner Agent

**Recommended mode:** `--autonomy cautious` for multi-step coordination

```bash
# Example: Orchestrate planning workflow with balanced autonomy
python3 scripts/orchestrate.py route task_definition --execute --adapter cli --autonomy cautious
```

### Reviewer Agent

**Audit verification workflow:**

1. Check audit log exists: `ls -la runs/autonomy-decisions.jsonl`
2. Verify appropriate mode was used
3. Check auto-approved decisions align with risk classifications
4. Confirm CRITICAL operations handled correctly

## Troubleshooting

### "Autonomy config not found" Error

**Problem:** `configs/autonomy.yaml` doesn't exist

**Solution:**
```bash
# Copy example config
cp configs/autonomy.yaml.example configs/autonomy.yaml

# Or let orchestrator fall back to legacy approval gates (backward compatible)
```

### Summary Shows 0 Auto-Approved

**Problem:** Timing issue in old versions (fixed in v1.2.0)

**Solution:** Upgrade to v1.2.0 or later

### CRITICAL Operations Blocked in Cautious Mode

**Expected behavior:** Cautious mode blocks CRITICAL by design

**Options:**
1. Use `--autonomy full` if you accept the risk
2. Break operation into smaller, lower-risk steps
3. Review `configs/autonomy.yaml` risk classifications

### Audit Log Growing Large

**Maintenance:**
```bash
# Archive old logs
mv runs/autonomy-decisions.jsonl runs/autonomy-decisions-2026-06.jsonl

# Or periodic cleanup
find runs -name "autonomy-decisions-*.jsonl" -mtime +90 -delete
```

## Best Practices

1. **Start with cautious mode** - balanced safety and efficiency
2. **Use ask mode** when learning or working in unfamiliar code
3. **Reserve full mode** for validated plans with comprehensive tests
4. **Always review audit logs** after critical operations
5. **Customize risk classifications** to match your project's risk tolerance
6. **Test with dry-run first** (`--dry-run` flag, no autonomy involved)
7. **Commit autonomy.yaml** to version control for team consistency

## See Also

- [Agent Contracts](../agents/) - Agent-specific autonomy guidance
- [Skills](../skills/) - Autonomy recommendations for workflows
- [Eval Case](../evals/cases/autonomy/basic-autonomy-modes.md) - Test scenarios
- [Rubric](../evals/rubrics/autonomy-behavior.md) - Quality criteria
- [Integration Tests](../scripts/orchestrator/tests/test_driver_autonomy.py) - Code examples
