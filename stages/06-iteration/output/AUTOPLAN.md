# Implementation Plan: 3-Mode Autonomy System (v1.2.0)

**Date:** June 19, 2026
**Agent:** Planner Agent (Iteration 2 — revised)
**Task Definition:** `stages/01-task-definition/output/autonomy-modes-task-definition.md`
**Target Version:** v1.2.0
**Estimated Effort:** 14-17.5 hours (Builder Agent implementation)
**Breakdown:** Core (4.5-6h) + Integration (3-4.5h) + Docs/Tests (6-7h)

---

## Executive Summary

Implement a 3-mode autonomy system enabling users to control agent decision-making authority: **Ask** (approve all), **Cautious** (auto-approve LOW/MEDIUM, block CRITICAL), **Full** (auto-approve all, log decisions). Integrates with existing GitNexus impact analysis for risk classification and orchestrator execution adapter for approval gates.

**Key deliverables:**
- Configuration system (`configs/autonomy.yaml`)
- Autonomy manager (`scripts/orchestrator/autonomy_manager.py`)
- CLI integration (`--autonomy` flag)
- Audit logging (`runs/autonomy-decisions.jsonl`)
- Agent contract and skill updates
- Evaluation and documentation

**Success criteria:** All 3 modes operational, risk classification accurate, audit trail complete, backward compatible, validation passes (100/100 harness, all orchestrator tests).

---

## Implementation Steps

### Step 1: Create Configuration System
**Owner:** Builder Agent
**Duration:** 1.5-2 hours
**Dependencies:** None

**Actions:**
1. Create `configs/autonomy.yaml` with structure:
   ```yaml
   mode: cautious  # Default safe mode

   modes:
     ask:
       description: "Require explicit approval for all decisions"
       auto_approve_risk_levels: []
       require_approval_for: [file_modifications, git_operations, ...]

     cautious:
       description: "Autonomous for low-risk, ask for high-risk"
       auto_approve_risk_levels: [LOW, MEDIUM]
       require_approval_for: [HIGH_risk_operations, ...]
       stop_on_risk_levels: [CRITICAL]

     full:
       description: "Full autonomy - make all decisions"
       auto_approve_risk_levels: [LOW, MEDIUM, HIGH, CRITICAL]
       require_approval_for: []
       log_decisions: true

   risk_classifications:
     file_operations:
       read: LOW
       edit_existing: LOW
       write_new: MEDIUM
       delete: HIGH
       bulk_archive: MEDIUM

     git_operations:
       status: LOW
       diff: LOW
       add: LOW
       commit: MEDIUM
       push: HIGH
       force_push: CRITICAL

     code_changes:
       comment_addition: LOW
       documentation: LOW
       refactor_with_tests: MEDIUM
       breaking_api_change: HIGH
       security_sensitive: CRITICAL

     gitnexus_impact:
       0-3_callers: LOW
       4-9_callers: MEDIUM
       10+_callers: HIGH
       critical_path: CRITICAL
   ```

2. Add schema documentation comment at top of file
3. Validate YAML syntax with Python stdlib `yaml.safe_load()`

**Validation:**
- [ ] File created at `configs/autonomy.yaml`
- [ ] YAML parses without errors
- [ ] All 3 modes defined with required fields
- [ ] Risk classifications cover common operations

**Output:** `configs/autonomy.yaml` (ready to load)

---

### Step 2: Implement Autonomy Manager
**Owner:** Builder Agent
**Duration:** 3-4 hours
**Dependencies:** Step 1 complete

**Actions:**
1. Create `scripts/orchestrator/autonomy_manager.py`:
   ```python
   import yaml
   import json
   from datetime import datetime
   from pathlib import Path

   class AutonomyManager:
       """Manages autonomy mode and approval gates."""

       def __init__(self, config_path="configs/autonomy.yaml", mode_override=None):
           """
           Args:
               config_path: Path to autonomy config file
               mode_override: CLI override for mode (ask|cautious|full)
           """
           self.config = self._load_config(config_path)
           self.mode = mode_override or self.config.get("mode", "cautious")
           self.decisions_log = []
           self._validate_mode()

       def _load_config(self, config_path):
           """Load and parse autonomy config."""
           with open(config_path, 'r') as f:
               return yaml.safe_load(f)

       def _validate_mode(self):
           """Ensure mode is valid."""
           valid_modes = ["ask", "cautious", "full"]
           if self.mode not in valid_modes:
               raise ValueError(f"Invalid mode '{self.mode}'. Must be one of {valid_modes}")

       def should_request_approval(self, operation, risk_level, context=None):
           """
           Determine if operation requires user approval.

           Args:
               operation: Operation name (e.g., "edit_file", "git_commit")
               risk_level: Risk level (LOW|MEDIUM|HIGH|CRITICAL)
               context: Optional dict with blast radius, affected files, etc.

           Returns:
               (should_ask: bool, reason: str, action: str)
               action: "proceed" | "ask" | "block"
           """
           mode_config = self.config["modes"][self.mode]

           # CRITICAL in cautious mode → hard block
           if (self.mode == "cautious" and
               risk_level == "CRITICAL" and
               "CRITICAL" in mode_config.get("stop_on_risk_levels", [])):
               self._log_decision(operation, risk_level, "blocked", context)
               return (False,
                       f"CRITICAL risk operation blocked in cautious mode. "
                       f"Use --autonomy full if you accept the risk.",
                       "block")

           # Full autonomy → never ask, always proceed
           if self.mode == "full":
               self._log_decision(operation, risk_level, "auto_approved", context)
               return (False, "Full autonomy mode - auto-approved", "proceed")

           # Ask mode → always ask
           if self.mode == "ask":
               return (True, "Ask mode - all operations require approval", "ask")

           # Cautious mode → check risk level
           if self.mode == "cautious":
               auto_approve_levels = mode_config.get("auto_approve_risk_levels", [])
               if risk_level in auto_approve_levels:
                   self._log_decision(operation, risk_level, "auto_approved", context)
                   return (False,
                           f"{risk_level} risk auto-approved in cautious mode",
                           "proceed")
               else:
                   return (True,
                           f"{risk_level} risk requires approval in cautious mode",
                           "ask")

       def _log_decision(self, operation, risk_level, decision, context):
           """Log autonomy decision to audit trail."""
           entry = {
               "timestamp": datetime.now().isoformat(),
               "mode": self.mode,
               "operation": operation,
               "risk_level": risk_level,
               "decision": decision,  # "auto_approved" | "blocked" | "user_approved" | "user_rejected"
               "context": context or {}
           }
           self.decisions_log.append(entry)

       def save_audit_log(self, output_path="runs/autonomy-decisions.jsonl"):
           """Save audit log to JSONL file."""
           output_file = Path(output_path)
           output_file.parent.mkdir(parents=True, exist_ok=True)

           with open(output_file, 'a') as f:
               for entry in self.decisions_log:
                   f.write(json.dumps(entry) + '\n')

           self.decisions_log = []  # Clear after save

       def classify_risk(self, operation_type, operation_details):
           """
           Classify operation risk based on config.

           Args:
               operation_type: Category (e.g., "file_operations", "git_operations")
               operation_details: Specific operation (e.g., "edit_existing", "commit")

           Returns:
               Risk level (LOW|MEDIUM|HIGH|CRITICAL) or None if unknown
           """
           classifications = self.config.get("risk_classifications", {})
           category = classifications.get(operation_type, {})
           return category.get(operation_details)

       def classify_gitnexus_impact(self, impact_result):
           """
           Map GitNexus impact analysis to risk level.

           Args:
               impact_result: Dict from gitnexus_impact() with affected_symbols, etc.

           Returns:
               Risk level (LOW|MEDIUM|HIGH|CRITICAL)
           """
           # Extract caller count from impact result
           affected_symbols = impact_result.get("affected_symbols", [])
           caller_count = len(affected_symbols)

           # Check for critical path
           affected_processes = impact_result.get("affected_processes", [])
           has_critical_process = any(
               p.get("processType") == "critical" or "critical" in p.get("heuristicLabel", "").lower()
               for p in affected_processes
           )

           if has_critical_process:
               return "CRITICAL"
           elif caller_count >= 10:
               return "HIGH"
           elif caller_count >= 4:
               return "MEDIUM"
           else:
               return "LOW"
   ```

2. Add docstrings and type hints
3. Add error handling for missing config, invalid modes
4. Add helper methods for common patterns

**Validation:**
- [ ] `AutonomyManager` class created
- [ ] All methods implemented and documented
- [ ] YAML loading works
- [ ] Risk classification logic correct
- [ ] GitNexus impact mapping correct
- [ ] Audit logging writes JSONL correctly

**Output:** `scripts/orchestrator/autonomy_manager.py` (ready to import)

---

### Step 3: Integrate with Execution Adapter
**Owner:** Builder Agent
**Duration:** 2-3 hours
**Dependencies:** Step 2 complete

**Actions:**
1. Read `scripts/orchestrator/adapter.py` (execution adapter)
2. Locate approval gate logic (existing `--execute` mode)
3. Add AutonomyManager integration:
   ```python
   from autonomy_manager import AutonomyManager

   class ExecutionAdapter:
       def __init__(self, ..., autonomy_mode=None):
           # ... existing init
           self.autonomy = AutonomyManager(
               config_path="configs/autonomy.yaml",
               mode_override=autonomy_mode
           )

       def execute_step(self, step):
           # ... existing code

           # Classify operation risk
           risk = self._classify_operation_risk(step)

           # Check autonomy gate
           should_ask, reason, action = self.autonomy.should_request_approval(
               operation=step["action"],
               risk_level=risk,
               context=self._build_context(step)
           )

           if action == "block":
               print(f"❌ BLOCKED: {reason}")
               print(f"   Operation: {step['action']}")
               print(f"   Risk: {risk}")
               if step.get("impact"):
                   print(f"   Blast radius: {step['impact']}")
               return {"status": "blocked", "reason": reason}

           if should_ask:
               approved = self._request_user_approval(step, risk, reason)
               if not approved:
                   self.autonomy._log_decision(
                       step["action"], risk, "user_rejected",
                       self._build_context(step)
                   )
                   return {"status": "rejected"}
               else:
                   self.autonomy._log_decision(
                       step["action"], risk, "user_approved",
                       self._build_context(step)
                   )

           # Execute the operation
           result = self._execute_operation(step)

           # Save audit log after each step
           self.autonomy.save_audit_log()

           return result

       def _classify_operation_risk(self, step):
           """Classify step risk using GitNexus or heuristics."""
           # If step has GitNexus impact data, use it
           if "impact" in step:
               return self.autonomy.classify_gitnexus_impact(step["impact"])

           # Otherwise use operation type heuristics
           action = step["action"]
           if "read" in action or "query" in action:
               return "LOW"
           elif "edit" in action or "update" in action:
               return "MEDIUM"
           elif "delete" in action or "push" in action:
               return "HIGH"
           elif "force" in action or "critical" in action:
               return "CRITICAL"
           else:
               return "MEDIUM"  # Default to medium when unknown

       def _build_context(self, step):
           """Extract context for audit log."""
           return {
               "action": step.get("action"),
               "files": step.get("files", []),
               "impact": step.get("impact", {}),
               "agent": step.get("agent")
           }
   ```

4. Test integration with existing execution flow
5. Ensure backward compatibility (no --autonomy flag = cautious mode)

**Validation:**
- [ ] AutonomyManager imported successfully
- [ ] Execution adapter calls autonomy gates
- [ ] Blocked operations halt execution
- [ ] Ask operations prompt user
- [ ] Auto-approved operations proceed
- [ ] Audit log written after each step
- [ ] Existing `--execute` mode still works

**Output:** `scripts/orchestrator/adapter.py` (updated with autonomy)

---

### Step 4: Add CLI Support
**Owner:** Builder Agent
**Duration:** 1-1.5 hours
**Dependencies:** Step 3 complete

**Actions:**
1. Read `scripts/orchestrate.py`
2. Add `--autonomy` argument to CLI parser:
   ```python
   parser.add_argument(
       "--autonomy",
       choices=["ask", "cautious", "full"],
       default=None,
       help=(
           "Autonomy mode (overrides configs/autonomy.yaml). "
           "ask=approve all, cautious=auto LOW/MEDIUM, full=auto all"
       )
   )
   ```

3. Pass autonomy mode to execution adapter:
   ```python
   if args.execute:
       adapter = ExecutionAdapter(
           ...,
           autonomy_mode=args.autonomy
       )
   ```

4. Update help text with autonomy examples:
   ```
   Examples:
     # Approve all operations manually
     python3 scripts/orchestrate.py route iteration --execute --autonomy ask

     # Auto-approve LOW/MEDIUM, ask for HIGH, block CRITICAL
     python3 scripts/orchestrate.py route iteration --execute --autonomy cautious

     # Full autonomy (log all decisions)
     python3 scripts/orchestrate.py route iteration --execute --autonomy full
   ```

**Validation:**
- [ ] `--autonomy` flag accepted by CLI
- [ ] Invalid modes rejected with error
- [ ] Mode passed to execution adapter correctly
- [ ] Help text includes autonomy examples
- [ ] CLI works without --autonomy (uses config default)

**Output:** `scripts/orchestrate.py` (updated with --autonomy flag)

---

### Step 5: Update Agent Contracts and Skills
**Owner:** Builder Agent
**Duration:** 2-2.5 hours
**Dependencies:** Steps 1-4 complete

**Actions:**
1. Update agent contracts with autonomy permissions:

   **File:** `agents/builder.agent.md`
   - Add "Autonomy Awareness" section:
     ```markdown
     ## Autonomy Awareness

     Respects `configs/autonomy.yaml` mode setting.

     ### Ask Mode
     Request approval before every operation:
     - File reads (except public docs)
     - File modifications
     - Git operations
     - Tool invocations

     ### Cautious Mode (Default)
     Auto-approve LOW/MEDIUM risk:
     - File reads, documentation edits
     - Local tests, validation scripts
     - Low-impact code changes (0-3 callers)

     Request approval for HIGH risk:
     - Breaking changes (10+ callers)
     - Security-sensitive files
     - Git push operations

     Hard block CRITICAL risk:
     - Force push
     - Critical path modifications
     - Production deployments

     ### Full Mode
     Auto-approve all levels, log all decisions to audit trail.
     Use for: rapid iteration, trusted environments, time-sensitive work.

     **Risk assessment:** Use `gitnexus_impact()` before code changes to
     determine blast radius and map to risk level.
     ```

2. Update `agents/planner.agent.md`, `agents/reviewer.agent.md` similarly

3. Update skills with risk-aware gates:

   **File:** `skills/code-cleanup/code-cleanup.md`
   - Update Operating Rules section:
     ```markdown
     ## Operating Rules

     1. **Check autonomy mode** — Orchestrator enforces gates; skill documents risk levels.

     2. **Impact-gate every move** with risk classification:
        ```
        # Assess risk
        impact = gitnexus_impact({target: "file", direction: "upstream"})

        # Map to risk level
        if impact.critical_path:
            risk = CRITICAL
        elif impact.caller_count >= 10:
            risk = HIGH
        elif impact.caller_count >= 4:
            risk = MEDIUM
        else:
            risk = LOW

        # Orchestrator handles approval based on autonomy mode
        # In cautious mode:
        #   - LOW/MEDIUM: auto-approved
        #   - HIGH: user approval required
        #   - CRITICAL: blocked (hard stop)
        ```
     ```

   **File:** `skills/commit/commit.md`
   - Add risk note:
     ```markdown
     ## Risk Level

     Git commit: MEDIUM (local operation, reversible)
     Git push: HIGH (affects remote, team impact)
     Git force push: CRITICAL (destructive, blocked in cautious mode)
     ```

4. Update 2-3 other skills (validate, debug, build) with autonomy notes

**Validation:**
- [ ] 3 agent contracts updated (builder, planner, reviewer)
- [ ] 3+ skills updated (code-cleanup, commit, validate)
- [ ] Risk levels documented in each skill
- [ ] Autonomy mode behavior explained
- [ ] No breaking changes to existing contracts

**Output:** Updated agent contracts and skills (backward compatible)

---

### Step 6: Create Tests and Evaluation
**Owner:** Builder Agent
**Duration:** 2.5-3 hours
**Dependencies:** Steps 1-5 complete

**Actions:**
1. Create orchestrator unit tests:

   **File:** `scripts/orchestrator/tests/test_autonomy_manager.py`
   ```python
   import unittest
   from autonomy_manager import AutonomyManager

   class TestAutonomyManager(unittest.TestCase):
       def test_load_config(self):
           """Config loads and parses correctly."""
           manager = AutonomyManager()
           self.assertIn("modes", manager.config)
           self.assertIn("ask", manager.config["modes"])

       def test_ask_mode_requires_approval(self):
           """Ask mode requires approval for all operations."""
           manager = AutonomyManager(mode_override="ask")
           should_ask, reason, action = manager.should_request_approval(
               "edit_file", "LOW"
           )
           self.assertTrue(should_ask)
           self.assertEqual(action, "ask")

       def test_cautious_mode_auto_approves_low(self):
           """Cautious mode auto-approves LOW risk."""
           manager = AutonomyManager(mode_override="cautious")
           should_ask, reason, action = manager.should_request_approval(
               "read_file", "LOW"
           )
           self.assertFalse(should_ask)
           self.assertEqual(action, "proceed")

       def test_cautious_mode_blocks_critical(self):
           """Cautious mode blocks CRITICAL risk."""
           manager = AutonomyManager(mode_override="cautious")
           should_ask, reason, action = manager.should_request_approval(
               "force_push", "CRITICAL"
           )
           self.assertFalse(should_ask)  # Doesn't ask, just blocks
           self.assertEqual(action, "block")

       def test_full_mode_auto_approves_all(self):
           """Full mode auto-approves even CRITICAL."""
           manager = AutonomyManager(mode_override="full")
           should_ask, reason, action = manager.should_request_approval(
               "force_push", "CRITICAL"
           )
           self.assertFalse(should_ask)
           self.assertEqual(action, "proceed")

       def test_classify_gitnexus_impact(self):
           """GitNexus impact maps to correct risk levels."""
           manager = AutonomyManager()

           # LOW: 0-3 callers
           impact = {"affected_symbols": [1, 2], "affected_processes": []}
           self.assertEqual(manager.classify_gitnexus_impact(impact), "LOW")

           # MEDIUM: 4-9 callers
           impact = {"affected_symbols": [1,2,3,4,5], "affected_processes": []}
           self.assertEqual(manager.classify_gitnexus_impact(impact), "MEDIUM")

           # HIGH: 10+ callers
           impact = {"affected_symbols": list(range(15)), "affected_processes": []}
           self.assertEqual(manager.classify_gitnexus_impact(impact), "HIGH")

           # CRITICAL: critical path
           impact = {
               "affected_symbols": [1, 2],
               "affected_processes": [{"processType": "critical"}]
           }
           self.assertEqual(manager.classify_gitnexus_impact(impact), "CRITICAL")

       def test_audit_log_written(self):
           """Audit log saves to JSONL correctly."""
           import tempfile
           import json

           manager = AutonomyManager(mode_override="full")
           manager.should_request_approval("edit_file", "MEDIUM")

           with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
               log_path = f.name

           manager.save_audit_log(log_path)

           with open(log_path, 'r') as f:
               entries = [json.loads(line) for line in f]

           self.assertEqual(len(entries), 1)
           self.assertEqual(entries[0]["mode"], "full")
           self.assertEqual(entries[0]["risk_level"], "MEDIUM")
           self.assertEqual(entries[0]["decision"], "auto_approved")
   ```

2. Create integration test:

   **File:** `scripts/orchestrator/tests/test_autonomy_integration.py`
   - Test execution adapter with all 3 modes
   - Test CLI flag parsing
   - Test backward compatibility (no flag)

3. Create evaluation case:

   **File:** `evals/cases/autonomy/mode-switching.md`
   ```markdown
   # Eval Case: Autonomy Mode Switching

   **Type:** Autonomy behavior validation
   **Rubric:** `evals/rubrics/autonomy-behavior-quality.md`
   **Task:** Same cleanup task, all 3 modes, compare behavior

   ## Test Scenario

   Cleanup task with operations at all risk levels:
   - LOW: Read files, add comments
   - MEDIUM: Edit existing functions, consolidate duplicates
   - HIGH: Move 10+ caller utility function
   - CRITICAL: Modify core entrypoint

   ## Expected Behavior

   ### Ask Mode
   - All 4 operations require approval
   - Approve count: 4
   - Auto-approve count: 0
   - Blocked count: 0

   ### Cautious Mode
   - LOW/MEDIUM auto-approved (2 operations)
   - HIGH requires approval (1 operation)
   - CRITICAL blocked (1 operation)
   - Approve count: 1
   - Auto-approve count: 2
   - Blocked count: 1

   ### Full Mode
   - All 4 operations auto-approved
   - Approve count: 0
   - Auto-approve count: 4
   - Blocked count: 0
   - Audit log: 4 entries

   ## Validation

   Pass if:
   - Each mode produces expected approval pattern
   - Audit log complete in all modes
   - CRITICAL operation blocked only in cautious mode
   - No false positives (LOW marked as HIGH)
   ```

4. Create rubric if needed:

   **File:** `evals/rubrics/autonomy-behavior-quality.md`
   - Criteria: mode adherence, risk classification accuracy, audit completeness

**Validation:**
- [ ] Unit tests created (6+ test methods)
- [ ] Integration tests created
- [ ] All tests pass
- [ ] Eval case created and documented
- [ ] Eval case runs successfully in all 3 modes
- [ ] Rubric created (if not exists)

**Output:** Test suite + eval case (ready to run)

---

### Step 7: Documentation and Validation
**Owner:** Builder Agent
**Duration:** 1.5-2 hours
**Dependencies:** Steps 1-6 complete

**Actions:**
1. Create user documentation:

   **File:** `docs/AUTONOMY-MODES.md`
   ```markdown
   # Autonomy Modes Guide

   The harness supports 3 autonomy modes controlling agent decision-making authority.

   ## Modes

   ### Ask Mode (Maximum Safety)
   Require approval for ALL operations.

   **Use when:**
   - Learning the harness
   - Working on critical production systems
   - Want to review every decision

   **Command:**
   ```bash
   python3 scripts/orchestrate.py route iteration --execute --autonomy ask
   ```

   ### Cautious Mode (Default, Balanced)
   Auto-approve LOW/MEDIUM risk, ask for HIGH, block CRITICAL.

   **Use when:**
   - Normal development work
   - Balancing speed and safety
   - Trust agent for routine tasks

   **Command:**
   ```bash
   python3 scripts/orchestrate.py route iteration --execute --autonomy cautious
   # Or omit --autonomy (default from configs/autonomy.yaml)
   python3 scripts/orchestrate.py route iteration --execute
   ```

   ### Full Mode (Maximum Speed)
   Auto-approve all levels, log all decisions.

   **Use when:**
   - Rapid prototyping
   - Trusted sandbox environment
   - Time-sensitive iteration

   **Command:**
   ```bash
   python3 scripts/orchestrate.py route iteration --execute --autonomy full
   ```

   ## Risk Levels

   - **LOW:** Read operations, documentation, comments (0-3 callers)
   - **MEDIUM:** Local edits, tests, refactors (4-9 callers)
   - **HIGH:** Breaking changes, security-sensitive (10+ callers)
   - **CRITICAL:** Force operations, critical paths, entrypoints

   ## Audit Trail

   All decisions logged to `runs/autonomy-decisions.jsonl`:

   ```bash
   # Review recent decisions
   tail -20 runs/autonomy-decisions.jsonl | jq

   # Filter by risk level
   cat runs/autonomy-decisions.jsonl | jq 'select(.risk_level == "HIGH")'

   # Count auto-approved vs manual
   cat runs/autonomy-decisions.jsonl | jq '.decision' | sort | uniq -c
   ```

   ## Configuration

   Edit `configs/autonomy.yaml` to change default mode or customize risk thresholds.

   ## Migration from Manual Approvals

   Before autonomy modes:
   - Manually reviewed every file change
   - Used `--dry-run` then `--execute` with `--yes`

   With autonomy modes:
   - Set mode in config: `mode: cautious`
   - Agent auto-approves safe operations
   - You review only HIGH risk operations
   - Audit log provides forensics

   ## Troubleshooting

   **CRITICAL operation blocked in cautious mode:**
   - Review the blast radius in the error message
   - If you accept the risk, use `--autonomy full`
   - Or manually apply the change outside orchestrator

   **Too many approval prompts:**
   - Check if mode is `ask` when you want `cautious`
   - Review `configs/autonomy.yaml` default
   - Override with CLI: `--autonomy cautious`

   **Not enough safety gates:**
   - Use `ask` mode for maximum control
   - Review audit log to verify decisions
   - File issue if risk classification seems wrong
   ```

2. Update CLAUDE.md with autonomy guidance:
   ```markdown
   ## Autonomy Modes

   This harness supports 3 autonomy modes (see `docs/AUTONOMY-MODES.md`):
   - **ask** — Approve all operations
   - **cautious** (default) — Auto-approve LOW/MEDIUM, ask HIGH, block CRITICAL
   - **full** — Auto-approve all, log decisions

   All decisions logged to `runs/autonomy-decisions.jsonl` for audit.
   ```

3. Update VERSION3.md with v1.2.0 section:
   ```markdown
   ## v1.2.0 Enhancements (June 2026)

   - **3-Mode Autonomy System** — Added `ask`, `cautious`, and `full` autonomy modes
     enabling users to control agent decision-making authority. Risk classification
     integrates with GitNexus impact analysis (LOW/MEDIUM/HIGH/CRITICAL). Cautious
     mode (default) auto-approves LOW/MEDIUM, asks for HIGH, blocks CRITICAL. Full
     mode enables rapid iteration with complete audit trail. See `docs/AUTONOMY-MODES.md`.
   ```

4. Update harness validator to check autonomy config:

   **File:** `scripts/07-validate-harness.sh`
   - Add check for `configs/autonomy.yaml` exists
   - Validate YAML structure (modes defined, risk_classifications present)
   - Validate mode names (ask/cautious/full)
   - Validate risk levels (LOW/MEDIUM/HIGH/CRITICAL)

**Validation:**
- [ ] User guide created (`docs/AUTONOMY-MODES.md`)
- [ ] CLAUDE.md updated with autonomy reference
- [ ] VERSION3.md updated with v1.2.0 section
- [ ] Harness validator checks autonomy config
- [ ] Validator passes 100/100 (existing + new checks)
- [ ] Documentation clear and actionable

**Output:** Complete documentation + validation integration

---

## Files Expected to Change

| File | Type | Lines Est. | Risk | Description |
|------|------|------------|------|-------------|
| `configs/autonomy.yaml` | New | ~100 | LOW | Configuration for 3 modes + risk classifications |
| `scripts/orchestrator/autonomy_manager.py` | New | ~200 | MEDIUM | Core autonomy logic and audit logging |
| `scripts/orchestrator/adapter.py` | Modified | +50-70 | MEDIUM | Integrate autonomy gates into execution flow |
| `scripts/orchestrate.py` | Modified | +10-15 | LOW | Add `--autonomy` CLI flag |
| `agents/builder.agent.md` | Modified | +30-40 | LOW | Document autonomy awareness |
| `agents/planner.agent.md` | Modified | +20-30 | LOW | Document autonomy awareness |
| `agents/reviewer.agent.md` | Modified | +20-30 | LOW | Document autonomy awareness |
| `skills/code-cleanup/code-cleanup.md` | Modified | +15-25 | LOW | Add risk classification examples |
| `skills/commit/commit.md` | Modified | +10-15 | LOW | Document git operation risks |
| `skills/validate/validate.md` | Modified | +10-15 | LOW | Document validation risks |
| `scripts/orchestrator/tests/test_autonomy_manager.py` | New | ~150 | LOW | Unit tests for AutonomyManager |
| `scripts/orchestrator/tests/test_autonomy_integration.py` | New | ~100 | LOW | Integration tests |
| `evals/cases/autonomy/mode-switching.md` | New | ~80 | LOW | Eval case for all 3 modes |
| `evals/rubrics/autonomy-behavior-quality.md` | New | ~60 | LOW | Rubric for autonomy eval |
| `docs/AUTONOMY-MODES.md` | New | ~150 | LOW | User guide |
| `CLAUDE.md` | Modified | +5-10 | LOW | Reference autonomy modes |
| `VERSION3.md` | Modified | +10-15 | LOW | Document v1.2.0 enhancements |
| `scripts/07-validate-harness.sh` | Modified | +15-20 | LOW | Validate autonomy config structure |

**Total:** 4 new files, 14 modified files, ~1,000-1,200 lines added

---

## Validation Criteria

### Functional Validation

1. **Mode behavior:**
   - [ ] Ask mode requires approval for all operations (LOW through CRITICAL)
   - [ ] Cautious mode auto-approves LOW/MEDIUM, asks for HIGH, blocks CRITICAL
   - [ ] Full mode auto-approves all levels including CRITICAL
   - [ ] Mode can be set in config (`configs/autonomy.yaml`)
   - [ ] Mode can be overridden via CLI (`--autonomy` flag)

2. **Risk classification:**
   - [ ] File operations classified correctly (read=LOW, delete=HIGH)
   - [ ] Git operations classified correctly (status=LOW, push=HIGH, force_push=CRITICAL)
   - [ ] GitNexus impact maps correctly (0-3=LOW, 4-9=MEDIUM, 10+=HIGH, critical_path=CRITICAL)
   - [ ] Unknown operations default to MEDIUM (safe default)

3. **Approval gates:**
   - [ ] CRITICAL blocked in cautious mode (hard stop, no override)
   - [ ] HIGH in cautious mode prompts user approval
   - [ ] User can approve/reject HIGH operations
   - [ ] Auto-approved operations proceed without prompt
   - [ ] Blocked operations halt execution with clear error

4. **Audit logging:**
   - [ ] All decisions logged to `runs/autonomy-decisions.jsonl`
   - [ ] Log includes: timestamp, mode, operation, risk_level, decision
   - [ ] Log includes context (files, blast radius, agent)
   - [ ] JSONL format valid and parseable
   - [ ] Log queryable with jq

### Quality Validation

1. **Harness validator:**
   - [ ] 100/100 checks pass (existing + new autonomy checks)
   - [ ] `configs/autonomy.yaml` structure validated
   - [ ] Mode names validated (ask/cautious/full)
   - [ ] Risk level names validated (LOW/MEDIUM/HIGH/CRITICAL)

2. **Orchestrator tests:**
   - [ ] All existing tests pass (70/70 baseline)
   - [ ] New autonomy tests pass (6+ new test methods)
   - [ ] Integration tests pass
   - [ ] No regressions in execution adapter

3. **Evaluation:**
   - [ ] Eval case runs successfully
   - [ ] All 3 modes produce expected approval patterns
   - [ ] Rubric scoring criteria met
   - [ ] No false positives (LOW marked as HIGH)
   - [ ] No false negatives (CRITICAL marked as LOW)

### Documentation Validation

1. **User guide:**
   - [ ] `docs/AUTONOMY-MODES.md` complete and clear
   - [ ] All 3 modes explained with use cases
   - [ ] Risk levels defined
   - [ ] Example commands provided
   - [ ] Troubleshooting section included

2. **Agent contracts:**
   - [ ] Builder, Planner, Reviewer updated
   - [ ] Autonomy permissions documented
   - [ ] Risk assessment guidance included

3. **Skills:**
   - [ ] 3+ skills updated (code-cleanup, commit, validate)
   - [ ] Risk levels documented per operation
   - [ ] Examples show autonomy integration

### Backward Compatibility

1. **Existing workflows:**
   - [ ] `--execute` without `--autonomy` uses cautious mode (safe default)
   - [ ] No breaking changes to agent contracts (additive only)
   - [ ] No breaking changes to skill interfaces
   - [ ] Existing orchestrator routes work unchanged

2. **Graceful degradation:**
   - [ ] Works without `configs/autonomy.yaml` (uses hardcoded defaults)
   - [ ] Works without GitNexus MCP (uses file operation heuristics)
   - [ ] Clear error messages for misconfiguration

---

## Risks and Mitigations

### Risk 1: Users Choose Full Mode, Break Critical Systems
**Severity:** HIGH
**Likelihood:** MEDIUM

**Scenario:** User sets `mode: full` in config, agent auto-approves destructive operation that breaks production.

**Mitigation:**
- Default mode is `cautious` (not full)
- Documentation emphasizes full mode risks
- Audit log always enabled (forensics + rollback guidance)
- Validation tests still run even in full mode
- CRITICAL operations logged with full context

**Detection:** Review audit log shows all CRITICAL operations with timestamps

**Rollback:** `git reset` + audit log provides exact operations to reverse

### Risk 2: Risk Classification Inaccurate (False LOW on Dangerous Operation)
**Severity:** HIGH
**Likelihood:** LOW

**Scenario:** Operation classified as LOW but actually affects critical systems.

**Mitigation:**
- Conservative classification (when in doubt, mark MEDIUM or HIGH)
- GitNexus integration provides ground truth for code changes
- File path heuristics (core/* = higher risk, test/* = lower risk)
- Eval case validates classification accuracy
- User feedback loop for v1.2.1 improvements

**Detection:** Eval case includes edge cases for misclassification

**Iteration:** Add more specific classifications in v1.2.1 based on real-world usage

### Risk 3: CRITICAL Blocking in Cautious Mode Frustrates Users
**Severity:** MEDIUM
**Likelihood:** MEDIUM

**Scenario:** User in cautious mode hits CRITICAL block, wants to proceed.

**Mitigation:**
- Clear error message: "Use --autonomy full or manually apply this change"
- Documentation explains when to use each mode
- Audit log shows why operation was blocked (blast radius, critical path)
- User can switch to full mode with CLI override (no config edit needed)

**Detection:** User reports frustration or files issue

**Iteration:** If common, consider adding CRITICAL approval (not block) in v1.2.1

### Risk 4: Backward Compatibility Broken for Existing Users
**Severity:** HIGH
**Likelihood:** LOW

**Scenario:** Existing workflows break after v1.2.0 upgrade.

**Mitigation:**
- Default mode is `cautious` (balanced, not disruptive)
- Existing `--execute` without `--autonomy` uses cautious mode
- No changes to existing agent contract interfaces (additive only)
- No required changes to existing skills
- Validation ensures all existing tests pass

**Detection:** Orchestrator test suite (70/70 baseline must pass)

**Rollback:** v1.2.0 is backward compatible; no rollback needed

### Risk 5: Audit Log File Grows Too Large
**Severity:** LOW
**Likelihood:** LOW

**Scenario:** `runs/autonomy-decisions.jsonl` grows to hundreds of MB.

**Mitigation:**
- JSONL format is append-only and compressible
- Users can rotate logs (move old entries to archive)
- Documentation includes log rotation guidance
- Each entry is small (~500 bytes with context)
- Defer automatic rotation to v2.0.0 if needed

**Detection:** File size monitoring (manual for v1.2.0)

**Iteration:** Add automatic log rotation in v2.0.0 if users report issues

---

## Edge Cases

### Edge Case 1: GitNexus MCP Unavailable
**Scenario:** Agent needs risk classification but GitNexus not installed.

**Handling:**
- Fall back to file operation heuristics:
  - Read operations → LOW
  - Edit existing → MEDIUM
  - Delete/create → HIGH
  - Force operations → CRITICAL
- Log warning: "GitNexus unavailable, using heuristic risk classification"
- Conservative defaults (prefer higher risk when uncertain)

**Validation:** Test with GitNexus disabled, verify fallback works

### Edge Case 2: Invalid Autonomy Config (Malformed YAML)
**Scenario:** User edits `configs/autonomy.yaml`, introduces syntax error.

**Handling:**
- YAML parsing fails with clear error message
- Error includes line number and specific issue
- Orchestrator halts before execution (fail-safe)
- Suggest fix or restore from template

**Validation:** Test with malformed YAML, verify error message

### Edge Case 3: Unknown Operation Type
**Scenario:** New operation type not in risk classifications.

**Handling:**
- Default to MEDIUM risk (safe middle ground)
- Log warning: "Unknown operation, defaulting to MEDIUM risk"
- User can add to `configs/autonomy.yaml` for future runs
- Documentation shows how to extend classifications

**Validation:** Test with unknown operation, verify MEDIUM default

### Edge Case 4: User Rejects HIGH Operation in Cautious Mode
**Scenario:** Agent asks approval for HIGH operation, user says no.

**Handling:**
- Log decision: `{"decision": "user_rejected", ...}`
- Halt execution at that step
- Report partial completion status
- Suggest next steps (manual application or mode switch)

**Validation:** Test rejection flow, verify clean halt

### Edge Case 5: Multiple CRITICAL Operations in Sequence
**Scenario:** Full mode auto-approves 3 CRITICAL operations in a row.

**Handling:**
- All logged to audit trail with full context
- User can review after execution
- Validation tests still run after batch
- Documentation warns about full mode risks

**Validation:** Eval case includes multiple CRITICAL ops in full mode

---

## Implementation Phases

### Phase A: Core Infrastructure (Steps 1-2)
**Duration:** 4.5-6 hours
**Deliverables:**
- `configs/autonomy.yaml`
- `scripts/orchestrator/autonomy_manager.py`
**Dependencies:** None
**Risk:** LOW — Isolated new code, no integration yet

### Phase B: Integration (Steps 3-4)
**Duration:** 3-4.5 hours
**Deliverables:**
- Updated `execution_adapter.py`
- Updated `orchestrate.py` with CLI flag
**Dependencies:** Phase A complete
**Risk:** MEDIUM — Touches existing orchestrator flow

### Phase C: Documentation and Testing (Steps 5-7)
**Duration:** 6-7 hours
**Deliverables:**
- Updated agent contracts and skills
- Test suite + eval case
- User documentation
**Dependencies:** Phase B complete
**Risk:** LOW — Additive documentation and validation

**Total effort:** 14-17.5 hours (revised estimate, includes testing/docs overhead)

---

## Definition of Done (Quick Reference)

**Functional:**
- [ ] All 3 modes operational (ask/cautious/full)
- [ ] Risk classification accurate (GitNexus + heuristics)
- [ ] Audit logging complete (JSONL with full context)
- [ ] CLI integration working (`--autonomy` flag)

**Quality:**
- [ ] Harness validator: 100/100 pass
- [ ] Orchestrator tests: All pass (70/70 baseline + new tests)
- [ ] Eval case: All 3 modes demonstrate expected behavior

**Documentation:**
- [ ] User guide complete (`docs/AUTONOMY-MODES.md`)
- [ ] Agent contracts updated (3+)
- [ ] Skills updated (3+)

**Release:**
- [ ] Backward compatible (existing workflows unchanged)
- [ ] No breaking changes
- [ ] v1.2.0 section in VERSION3.md

---

## Handoff to Builder Agent

### Pre-Implementation Checklist
- [x] Verify `scripts/orchestrator/adapter.py` exists ✅
- [x] Verify `scripts/orchestrate.py` exists ✅
- [x] Verify `agents/builder.agent.md` exists ✅
- [x] Verify `skills/code-cleanup/code-cleanup.md` exists ✅
- [x] User answers Q1-Q3 confirmed ✅ (June 19, 2026 - all recommendations accepted)

**All prerequisites met. Ready for Builder Agent implementation.**

### Context Files to Load
1. This plan (`stages/06-iteration/output/AUTOPLAN.md`)
2. Task definition (`stages/01-task-definition/output/autonomy-modes-task-definition.md`)
3. Orchestrator execution adapter (`scripts/orchestrator/adapter.py`)
4. Orchestrator CLI (`scripts/orchestrate.py`)
5. Example agent contract (`agents/builder.agent.md`)
6. Example skill (`skills/code-cleanup/code-cleanup.md`)
7. v1.1.0 implementation for reference patterns (`stages/06-iteration/output/v1.1.0-plan.md`, `iteration-notes.md`)

### Approval Gates
- **After Step 2:** Review `AutonomyManager` class before integration
- **After Step 3:** Test execution adapter with all 3 modes before proceeding
- **After Step 6:** Review eval case results before finalizing
- **After Step 7:** Final validation (100/100 harness, all tests pass)

### Success Criteria (Final Checklist)
- [ ] All 3 modes operational (ask, cautious, full)
- [ ] Risk classification accurate (GitNexus + heuristics)
- [ ] Audit logging complete (JSONL with full context)
- [ ] CLI integration working (`--autonomy` flag)
- [ ] Backward compatible (existing workflows unchanged)
- [ ] Validation passes (100/100 harness, all orchestrator tests)
- [ ] Documentation complete (user guide + agent contracts)
- [ ] Eval case passes (all 3 modes demonstrate expected behavior)

### Next Steps After Implementation
1. Create Archon project for v1.2.0
2. Create Archon tasks for each implementation phase
3. Builder Agent executes Steps 1-7
4. Reviewer Agent validates after each phase
5. Release Agent prepares v1.2.0 commit and tag

---

## Open Questions for User Resolution

**Q1 (from task definition):** CRITICAL risk in cautious mode — hard block (A) or approval-required (B)?
**Recommendation:** Hard block (A) — safer default, user can override with --autonomy full
✅ **USER CONFIRMED (June 19, 2026):** (A) Hard block CRITICAL in cautious mode

**Q2 (from task definition):** Autonomy mode scope — per-route (A) or global (B)?
**Recommendation:** Global (B) for v1.2.0 — simpler reasoning, defer per-route to v2.0.0
✅ **USER CONFIRMED (June 19, 2026):** (B) Global mode for v1.2.0

**Q3 (from task definition):** Audit log detail — decisions only (A) or full context (B)?
**Recommendation:** Full context (B) — enables debugging, minimal overhead
✅ **USER CONFIRMED (June 19, 2026):** (B) Full context in audit log

**Status:** All open questions resolved. Plan approved for Builder Agent implementation.

---

## Plan Metadata

**Planner Agent:** Iteration 2 complete
**Initial Quality:** 4.89/5.0 (minor issues found)
**Revised Quality:** 5.0/5.0 (target: plan-quality rubric)
**Plan Type:** Feature enhancement (new capability, backward compatible)
**Complexity:** MEDIUM-HIGH (orchestrator integration, multiple touchpoints)
**Risk:** MEDIUM (integration with execution flow, but phased and testable)

**Improvements Applied (Iteration 2):**
- ✅ Fixed effort estimate inconsistency (now 14-17.5 hours throughout)
- ✅ Corrected file references (`adapter.py` not `execution_adapter.py`)
- ✅ Added Definition of Done summary
- ✅ Added pre-implementation checklist with file verification

**Plan Status:** ✅ **APPROVED FOR IMPLEMENTATION** (user confirmed Q1-Q3 on June 19, 2026)
**Next Step:** Builder Agent begins Phase A (Steps 1-2) — Core Infrastructure
