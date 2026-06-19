# Task Definition: 3-Mode Autonomy System

**Date:** June 19, 2026
**Agent:** Researcher Agent
**Context:** Post-v1.1.0 enhancement to enable flexible agent autonomy levels

---

## Task Overview

**Goal:** Implement a 3-mode autonomy system (Ask, Cautious, Full) that allows users to control how much decision-making authority agents have during workflow execution.

**Type:** Feature enhancement (adds new capability to harness)

**Scope:** Harness framework enhancement with backward compatibility

---

## Target Artifact

**Primary deliverable:** 3-mode autonomy system integrated into the harness execution layer

**Artifact type:** Framework enhancement + configuration system

**Components:**
- Configuration layer (`configs/autonomy.yaml`)
- Orchestrator integration (`scripts/orchestrator/autonomy_manager.py`)
- Agent contract updates (autonomy permissions)
- Skill integration (risk-aware approval gates)
- CLI support (`--autonomy` flag)
- Documentation and evaluation

---

## Success Criteria

1. ✅ **Three modes operational:**
   - **Ask mode:** Requires approval for all operations
   - **Cautious mode:** Auto-approves LOW/MEDIUM, asks for HIGH, blocks CRITICAL
   - **Full mode:** Auto-approves all levels, logs all decisions

2. ✅ **Risk classification system:**
   - Operations classified as LOW/MEDIUM/HIGH/CRITICAL
   - GitNexus impact analysis maps to risk levels
   - Clear thresholds documented in `configs/autonomy.yaml`

3. ✅ **Audit trail:**
   - All autonomy decisions logged to `runs/autonomy-decisions.jsonl`
   - Includes: timestamp, mode, operation, risk level, approval status
   - Queryable for post-execution review

4. ✅ **CLI integration:**
   - `--autonomy ask|cautious|full` flag works
   - Overrides config file when specified
   - Works with existing `--execute` mode

5. ✅ **Backward compatibility:**
   - Existing workflows work without autonomy config
   - Default mode: `cautious` (safe default)
   - No breaking changes to existing agent contracts or skills

6. ✅ **Validation passes:**
   - Harness validator: 100/100 checks pass
   - Orchestrator tests: All existing + new autonomy tests pass
   - Eval case demonstrates all 3 modes on same task

---

## Scope Boundaries

### In Scope

- Configuration system for 3 autonomy modes
- Risk classification for common operations (file ops, git ops, code changes)
- Integration with existing GitNexus impact analysis
- Orchestrator execution adapter updates
- CLI flag support
- Audit logging system
- Agent contract documentation updates
- Skill integration (code-cleanup, commit, validate as examples)
- Evaluation case for mode switching
- User documentation

### Out of Scope

- **UI/dashboard for autonomy decisions** — CLI/config only for v1.2.0
- **Custom risk thresholds per project** — Use hardcoded thresholds in v1.2.0, defer custom to v2.0.0
- **Rollback automation** — Log decisions but manual rollback (git reset) for v1.2.0
- **Multi-agent autonomy coordination** — Single-agent modes only, defer coordination to v2.0.0
- **Skill-specific autonomy overrides** — Global mode only, defer per-skill to v2.0.0

### Deferred (Future Versions)

- **v1.3.0:** Custom risk thresholds per project (project-specific `autonomy.yaml`)
- **v2.0.0:** Multi-agent autonomy coordination, per-skill autonomy overrides
- **v2.1.0:** Web UI for autonomy decision review and approval

---

## Context and Dependencies

### Related Work

- **GitNexus integration (v1.1.0):** Already provides impact analysis with blast radius
- **Orchestrator execution adapter (v1.0.0 Phase 04):** Already has `--execute` mode with approval gates
- **Tool permissions (v1.0.0):** Already has `configs/tools.yaml` for destructive command gates

### Dependencies

1. **GitNexus MCP** — Required for code change risk assessment
2. **Orchestrator Phase 04** — Execution adapter must be functional
3. **Python 3.8+** — For orchestrator runtime
4. **YAML parsing** — Already in orchestrator stdlib

### Integration Points

- `scripts/orchestrator/execution_adapter.py` — Add autonomy gate checks
- `configs/autonomy.yaml` — New config file (user-editable)
- `scripts/orchestrate.py` — Add `--autonomy` CLI flag
- Agent contracts — Document autonomy behavior
- Skills — Add risk-aware approval gates where needed

---

## Constraints

### Technical

- Must use Python stdlib only (no new dependencies)
- Must integrate with existing orchestrator execution flow
- Must preserve backward compatibility (default: cautious mode)
- Must work with or without GitNexus MCP (graceful degradation)

### User Experience

- Clear error messages when CRITICAL risk blocked in cautious mode
- Audit log must be human-readable (JSONL format)
- CLI help text must explain all 3 modes clearly
- Documentation must include migration guide from manual approvals

### Quality

- All existing tests must pass unchanged
- New tests required for each autonomy mode
- Eval case must demonstrate mode differences clearly
- Harness validator must check autonomy config structure

---

## Assumptions

1. ✅ **Users understand risk levels** — Documentation will explain LOW/MEDIUM/HIGH/CRITICAL
2. ✅ **GitNexus MCP available** — Graceful degradation if not (use file-count heuristics)
3. ✅ **Users want control** — Three modes cover spectrum from max-safety to max-speed
4. ✅ **Audit logging sufficient** — JSONL format meets observability needs
5. ✅ **Cautious mode is safe default** — Blocks CRITICAL, asks for HIGH

---

## Open Questions

### For User (James)

**Q1:** Should CRITICAL risk operations in cautious mode be:
- (A) **Hard blocked** — Agent cannot proceed even with approval (safer)
- (B) **Approval required** — Agent asks but allows user override (flexible)

**Recommendation:** (A) Hard blocked — If it's CRITICAL, forcing manual intervention is safer. User can switch to `--autonomy full` if they accept the risk.

✅ **CONFIRMED (June 19, 2026):** (A) Hard blocked — CRITICAL operations blocked in cautious mode

**Q2:** Should autonomy mode be:
- (A) **Per-route** — Different modes for different lifecycle stages
- (B) **Global** — One mode for entire execution

**Recommendation:** (B) Global for v1.2.0 — Simpler to reason about. Defer per-route to v2.0.0.

✅ **CONFIRMED (June 19, 2026):** (B) Global mode for v1.2.0

**Q3:** Should audit log include:
- (A) **Decisions only** — What was approved/rejected
- (B) **Full context** — Decision + risk assessment + blast radius details

**Recommendation:** (B) Full context — Enables post-execution review and debugging. Minimal overhead (JSONL append).

✅ **CONFIRMED (June 19, 2026):** (B) Full context in audit log

### For Builder (Implementation Decisions)

**Q4:** Risk classification for operations without GitNexus impact data?
- Use file operation heuristics (read=LOW, edit=MEDIUM, delete=HIGH)
- Use file path patterns (test/*=LOW, core/*=HIGH)
- Combination of both

**Q5:** Should autonomy mode persist across sessions?
- Stored in `configs/autonomy.yaml` (persistent)
- CLI flag only (ephemeral)
- Both (CLI overrides config)

**Recommendation:** Both — Config for default, CLI for one-time overrides

---

## Risks and Mitigations

### Risk 1: Users choose Full mode and break critical systems
**Severity:** HIGH
**Likelihood:** MEDIUM
**Mitigation:**
- Default to `cautious` mode (not full)
- Documentation emphasizes full mode risks
- Audit log always enabled (forensics)
- Validation tests still run even in full mode

### Risk 2: Risk classification inaccurate (false LOW on dangerous operation)
**Severity:** HIGH
**Likelihood:** LOW
**Mitigation:**
- Conservative classification (when in doubt, mark HIGH)
- GitNexus integration provides ground truth for code changes
- Eval case validates risk classification accuracy
- Iteration in v1.2.1 based on user feedback

### Risk 3: CRITICAL blocking in cautious mode frustrates users
**Severity:** MEDIUM
**Likelihood:** MEDIUM
**Mitigation:**
- Clear error message: "Use --autonomy full or manually apply this change"
- Document when to use each mode
- Provide audit log showing why it was blocked

### Risk 4: Backward compatibility broken for existing users
**Severity:** HIGH
**Likelihood:** LOW
**Mitigation:**
- Default mode is `cautious` (balanced, not disruptive)
- Existing `--execute` without `--autonomy` uses cautious mode
- No changes to existing agent contracts required (additive only)

---

## Validation Approach

### Functional Validation

1. **Mode behavior:**
   - Create test task with LOW/MEDIUM/HIGH/CRITICAL operations
   - Run with `--autonomy ask` → All require approval
   - Run with `--autonomy cautious` → LOW/MEDIUM auto, HIGH ask, CRITICAL block
   - Run with `--autonomy full` → All auto-approved

2. **Risk classification:**
   - Verify GitNexus impact → risk mapping correct
   - Test edge cases (no GitNexus, unknown file type)
   - Validate file operation risk levels

3. **Audit logging:**
   - Check `runs/autonomy-decisions.jsonl` created
   - Verify all fields present (timestamp, mode, operation, risk, approval)
   - Test JSONL parsing and querying

### Quality Validation

1. **Harness validator:**
   - Add checks for `configs/autonomy.yaml` structure
   - Verify mode names valid (ask/cautious/full)
   - Check risk level names valid (LOW/MEDIUM/HIGH/CRITICAL)

2. **Orchestrator tests:**
   - Unit tests for `AutonomyManager` class
   - Integration tests for execution adapter
   - End-to-end tests for all 3 modes

3. **Eval case:**
   - `evals/cases/autonomy/mode-switching.md`
   - Same task, all 3 modes, compare behavior
   - Rubric: autonomy-behavior-quality

### Documentation Validation

1. **User documentation:**
   - `docs/AUTONOMY-MODES.md` explains all 3 modes
   - Examples show when to use each mode
   - Migration guide from manual approvals

2. **Agent contracts:**
   - Each agent documents autonomy behavior
   - Permissions section references autonomy config

3. **Skills:**
   - Updated skills show risk-aware gates
   - Examples demonstrate autonomy integration

---

## Follow-Up Tasks

### After Implementation

1. **User acceptance testing** — Apply to real project with all 3 modes
2. **Dogfooding** — Use harness on itself with autonomy modes
3. **Documentation review** — Ensure examples are clear
4. **Archon task tracking** — Update status as phases complete

### Future Iterations (v1.2.1+)

1. **Risk classification refinement** — Based on user feedback
2. **Custom thresholds** — Per-project autonomy config
3. **Per-skill overrides** — Different modes for different skills
4. **Multi-agent coordination** — Autonomy handoffs between agents

---

## Definition of Done

- [ ] `configs/autonomy.yaml` created with 3 modes and risk classifications
- [ ] `scripts/orchestrator/autonomy_manager.py` implemented and tested
- [ ] Execution adapter integrated with autonomy gates
- [ ] CLI `--autonomy` flag functional
- [ ] Audit logging operational (`runs/autonomy-decisions.jsonl`)
- [ ] Agent contracts updated with autonomy permissions
- [ ] 3+ skills integrated (code-cleanup, commit, validate)
- [ ] Harness validator checks autonomy config (100/100 pass)
- [ ] Orchestrator tests pass (all existing + new autonomy tests)
- [ ] Eval case created and passes (`evals/cases/autonomy/mode-switching.md`)
- [ ] Documentation complete (`docs/AUTONOMY-MODES.md`)
- [ ] Backward compatibility verified (existing workflows unchanged)
- [ ] Archon tasks created and tracking enabled

---

## Checkpoint: User Confirmation Required

**Please confirm:**

1. **Q1 answer:** CRITICAL risk in cautious mode should be hard blocked (A)?
2. **Q2 answer:** Global autonomy mode for v1.2.0 (B)?
3. **Q3 answer:** Audit log includes full context (B)?
4. **Scope approval:** In/out scope boundaries acceptable?
5. **Risk mitigation:** Mitigations for identified risks sufficient?

**Once confirmed, this task definition is ready for handoff to Planner Agent for AUTOPLAN.md creation.**
