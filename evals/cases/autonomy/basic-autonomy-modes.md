# Eval Case: Basic Autonomy Modes

## Purpose

Test whether the 3-mode autonomy system (ask, cautious, full) correctly controls approval behavior during orchestrator execution and produces accurate audit logs.

## Input

Execute the `release` route with each of the three autonomy modes and verify:

1. **Ask mode**: All operations require approval
2. **Cautious mode**: LOW/MEDIUM auto-approved, HIGH requires approval, CRITICAL blocked
3. **Full mode**: All operations auto-approved

## Test Scenarios

### Scenario 1: Cautious Mode (Default)

```bash
python3 scripts/orchestrate.py route release --execute --adapter noop --yes
```

**Expected behavior:**
- Autonomy mode prints: "cautious (Autonomous for low-risk, ask for high-risk, block critical)"
- MEDIUM risk operations auto-approved
- Audit log created at `runs/autonomy-decisions.jsonl`
- Summary shows: N auto-approved, 0 user-approved, 0 rejected, 0 blocked

### Scenario 2: Full Mode

```bash
python3 scripts/orchestrate.py route iteration --execute --adapter noop --autonomy full --yes --max-steps 2
```

**Expected behavior:**
- Autonomy mode prints: "full (Full autonomy - make all decisions)"
- All risk levels auto-approved (LOW, MEDIUM, HIGH, CRITICAL)
- Audit log entries show mode="full" and decision="auto_approved"
- Summary shows: N auto-approved, 0 user-approved, 0 rejected, 0 blocked

### Scenario 3: Ask Mode (Interactive)

```bash
python3 scripts/orchestrate.py route release --execute --adapter noop --autonomy ask
```

**Expected behavior:**
- Autonomy mode prints: "ask (Require explicit approval for all decisions)"
- Prompts for approval on every step regardless of risk level
- User rejection halts execution
- Audit log shows decision="user_approved" or "user_rejected"

### Scenario 4: Backward Compatibility

```bash
# Temporarily rename configs/autonomy.yaml
mv configs/autonomy.yaml configs/autonomy.yaml.backup
python3 scripts/orchestrate.py route release --execute --adapter noop --yes
mv configs/autonomy.yaml.backup configs/autonomy.yaml
```

**Expected behavior:**
- No autonomy initialization message
- Falls back to legacy approval gates
- Execution completes successfully
- No audit log created

## Expected Qualities

### Risk Classification
- Operations correctly classified by risk level
- Protected writes (agents/, configs/, scripts/orchestrator/) marked HIGH
- Gated actions (from configs/tools.yaml) marked HIGH
- Heuristic fallback works when GitNexus unavailable

### Audit Logging
- JSONL format (one JSON object per line)
- Required fields: timestamp, mode, operation, risk_level, decision, context
- Context includes: step, agent, stage, outputs, gated, protected
- Log persists across runs (append mode)
- Summary accurate before log cleared

### Mode Behavior
- **Ask**: Always prompts (never auto-approves)
- **Cautious**: Auto-approves LOW/MEDIUM, asks for HIGH, blocks CRITICAL
- **Full**: Auto-approves all (LOG/MEDIUM/HIGH/CRITICAL)

### CLI Integration
- `--autonomy` flag accepts ask/cautious/full
- Flag overrides config default
- Help text displays correctly
- Invalid mode shows error

## Rubric

Use `evals/rubrics/autonomy-behavior.md`.

## Validation Commands

```bash
# Run all autonomy unit tests
python3 -m pytest scripts/orchestrator/tests/test_autonomy_manager.py -v

# Run integration tests
python3 -m pytest scripts/orchestrator/tests/test_driver_autonomy.py -v

# View audit log
cat runs/autonomy-decisions.jsonl | python3 -c "import sys, json; [print(json.dumps(json.loads(l), indent=2)) for l in sys.stdin]"

# Verify summary counts
tail -1 runs/autonomy-decisions.jsonl | python3 -c "import sys, json; entry = json.loads(sys.stdin.read()); print(f\"Last decision: {entry['decision']} for {entry['risk_level']} risk {entry['operation']}\")"
```

## Success Criteria

- ✅ All 24 unit tests pass
- ✅ All 7 integration tests pass
- ✅ All 3 modes behave correctly in manual testing
- ✅ Audit log format validates against schema
- ✅ Backward compatibility confirmed (no autonomy.yaml)
- ✅ CLI help displays --autonomy flag
- ✅ Summary counts match audit log entries
