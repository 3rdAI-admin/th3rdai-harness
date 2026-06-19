# AI Agent Development Harness Alignment Plan - Version 3

> **📋 For detailed release notes and migration guides, see [CHANGELOG.md](./CHANGELOG.md)**

## Overview

This version aligns the repository around a plain-text, model-agnostic development harness for AI agents and model workflows.

The goal is to route work through explicit framework layers:

- Agents
- Skills
- Prompts
- Models
- Configs
- Evals
- Runs
- Telemetry
- Lifecycle stages

The template now supports designing, implementing, evaluating, iterating, and releasing agent/model workflows with inspectable context and human review checkpoints.

## Core Lifecycle

```text
Task Definition → Agent Design → Prompt Design → Tool Integration → Evaluation → Iteration → Release
```

## Core Framework Layers

### 1. Framework Definition

**File:** `FRAMEWORK.md`

Defines the core concepts: agent, skill, prompt, model profile, evaluation, and run.

### 2. Agent Contracts

**Folder:** `agents/`

Agents are role-based actors with explicit responsibilities, permissions, outputs, and handoffs.

Default agents:

- Researcher
- Planner
- Builder
- Reviewer
- Evaluator

### 3. Skills

**Folder:** `skills/`

Skills remain reusable procedures an agent can follow.

Current core skills:

- `research`
- `plan`
- `plan-reviewer`
- `build`
- `eval`
- `validate`
- `debug`
- `revise`
- `run`
- `tests`
- `prompt`
- `commit`

### 4. Prompt Registry

**Folder:** `prompts/`

Prompts are versioned instruction templates with changelogs.

Prompt tracks (one per agent):

- `prompts/researcher/`
- `prompts/planner/`
- `prompts/builder/`
- `prompts/reviewer/`
- `prompts/evaluator/`
- `prompts/registry.md`

### 5. Model Profiles

**Folder:** `models/`

Model documentation records supported providers, model selection criteria, local model guidance, and comparison notes.

Configuration lives in `configs/models.yaml`.

### 6. Evaluations

**Folder:** `evals/`

Evals are first-class artifacts used to measure agent, prompt, skill, and model quality.

Rubrics:

- `evals/rubrics/plan-quality.md`
- `evals/rubrics/tool-safety.md`
- `evals/rubrics/agent-output-quality.md`
- `evals/rubrics/orchestrator-output-quality.md` — scores Native Orchestrator artifacts (config parses, context bundles, run records)

Cases (one or more per rubric):

- `evals/cases/planning/basic-feature-plan.md`
- `evals/cases/prompt-design/prompt-revision.md`
- `evals/cases/code-review/security-bug-review.md`
- `evals/cases/agent-handoff/planner-to-builder.md`
- `evals/cases/debugging/failing-test-diagnosis.md`
- `evals/cases/tool-safety/destructive-command-request.md`
- `evals/cases/orchestrator/{config-subset-parsing,run-record-fidelity,route-context-bundle}.md`

`evals/README.md` holds a registry of rubrics and cases. `scripts/07-validate-harness.sh` enforces that every case references a rubric that resolves. Model-comparison results use `evals/results/_TEMPLATE-model-comparison.md`.

### 7. Runs and Telemetry

**Folders:** `runs/`, `telemetry/`

Runs record execution history. Telemetry defines run-log conventions and observability guidance.

Use `telemetry/run-log-schema.md` when recording agent, prompt, model, or eval runs. Worked examples live in `runs/examples/`.

## Lifecycle Stage Reference

### Stage 01: Task Definition

**Folder:** `stages/01-task-definition/`

Clarifies the task, artifact type, scope, constraints, success criteria, assumptions, and open questions.

### Stage 02: Agent Design

**Folder:** `stages/02-agent-design/`

Creates or revises agent contracts, permissions, outputs, success criteria, and handoff rules.

### Stage 03: Prompt Design

**Folder:** `stages/03-prompt-design/`

Creates or revises versioned prompts, changelogs, and prompt registry entries.

### Stage 04: Tool Integration

**Folder:** `stages/04-tool-integration/`

Defines tool permissions, runtime behavior, scripts, integrations, and safety policies.

### Stage 05: Evaluation

**Folder:** `stages/05-evaluation/`

Applies rubrics and representative cases to measure agent, prompt, skill, and model performance.

### Stage 06: Iteration

**Folder:** `stages/06-iteration/`

Improves artifacts based on review or evaluation findings.

### Stage 07: Release

**Folder:** `stages/07-release/`

Prepares stable artifacts for use, documentation, or approved commit.

## Native Orchestrator (Optional Run Driver)

**Folder:** `scripts/orchestrator/` · **Effort spec:** `plans/native-orchestrator/`

The harness is agent-driven by default: a human or AI assistant follows
`configs/routing.yaml` and the stage contracts by hand. The Native Orchestrator
is an **optional**, dependency-free (Python stdlib only) driver that automates
the bookkeeping around that workflow. It is a **coordinator, not an executor** —
it assembles per-step context bundles and records runs; it does not itself call
a model or make decisions. All paths are resolved relative to a detected repo
root; no absolute paths are persisted.

| Phase | Plan | Delivers | Status |
|-------|------|----------|--------|
| 01 | `plans/native-orchestrator/01-config-and-runlog.md` | Stdlib YAML-subset config reader + run-record writer | done |
| 02 | `plans/native-orchestrator/02-sequencer.md` | Resolve a route into ordered, contract-backed steps + context bundles (dry-run) | done |
| 03 | `plans/native-orchestrator/03-cli-and-eval-hook.md` | `scripts/orchestrate.py` CLI + eval-case hook | done |
| 04 | `plans/native-orchestrator/04-execution-adapter.md` | Opt-in, approval-gated execution adapter (`--execute`) | done |

Dry-run is the default. Phase 04 adds opt-in execution via `configs/execution.yaml`
(this repo: `claude -p` with scrubbed env + `env_allowlist`). `--execute` honors
`configs/tools.yaml` approval gates, performs no autonomous commits, and forbids
self-modification without approval. UAT: `evals/results/20260529-orchestrator-phase-04-execute-uat.md`;
dogfood: `evals/results/20260530-orchestrator-dogfood-and-error-handling.md`.

## ICM Pedagogical Enhancements (Optional)

**Completed June 16, 2026** — Commits: 7ef2d98, 1e3bd6e, 4169036

Interpretable Context Methodology (ICM) enhancements improve harness onboarding, navigation, and distribution:

| Component | Artifact | Purpose |
|-----------|----------|---------|
| **Distribution modes** | README "Use This Harness" section | GitHub template, local scaffold, attach to existing app |
| **Bootstrap enhancements** | `scripts/01-create-project.sh` | `--with-orchestrator` flag, non-interactive mode (env vars), help text |
| **Release automation** | `scripts/08-prepare-template-release.sh` | Pre-release validation (harness + orchestrator + bootstrap dry-run) |
| **Navigation guide** | `docs/QUICK-REFERENCE.md` | 5-layer navigation model, common commands, lifecycle quick lookup, pitfalls |
| **Naming standards** | `_config/conventions.md` | File naming, slugification, load indicators, commit format |
| **Testing permissions** | `.claude/settings.json` | Pre-approved commands for harness development workflow |

**Validation:** 100 passed, 2 optional warnings (security-baseline forward reference, token budget columns deferred to Phase 2).

**Phase 2 (optional, deferred):** Add `Tokens (est.)` columns to stage CONTEXT.md files for explicit token budgeting.

## Recommended Workflow Paths

### Create a New Agent

1. `stages/01-task-definition/`
2. `stages/02-agent-design/`
3. Update `agents/<name>.agent.md`
4. Update `configs/agents.yaml`
5. Add or select eval rubric
6. Run evaluation
7. Release

### Create or Improve a Prompt

1. `stages/01-task-definition/`
2. `stages/03-prompt-design/`
3. Add `prompts/<name>/vN.md`
4. Update changelog and registry
5. Run relevant eval
6. Iterate if needed
7. Release

### Compare Models

1. Define the task and eval case
2. Select model profiles in `configs/models.yaml`
3. Run the same eval case across models
4. Record results in `evals/results/`
5. Update `models/model-matrix.md`

## Validation

Run:

```bash
scripts/07-validate-harness.sh                                    # Harness structure + cross-refs (100 checks)
python3 -m unittest discover scripts/orchestrator/tests           # Orchestrator unit tests (70 tests)
scripts/08-prepare-template-release.sh                            # Pre-release validation (all of the above + bootstrap)
```

The validator checks structure, cross-references (agent ↔ skill ↔ prompt ↔ config ↔
model profile), stage-contract coherence, skill path resolution, eval case ↔ rubric
coherence, and optional ICM enhancements (conventions.md, QUICK-REFERENCE.md, token budgets).
The Native Orchestrator has stdlib unit tests under `scripts/orchestrator/tests/`.
The release script performs a full validation sweep plus a dry-run bootstrap to a temp directory.

## Safety Principles

- Keep destructive actions behind explicit approval.
- Do not read secrets unnecessarily.
- Do not install dependencies without approval.
- Do not stage or commit without approval.
- Record skipped validation honestly.
- Treat eval failures as evidence for iteration.

## Completed (earlier milestones)

The following were completed and are no longer pending:

- Bootstrap scripts (`scripts/01`–`08`) generate the full agent harness structure and validate template releases.
- Native Orchestrator Phases 01–04 (config, sequencer, CLI, execution adapter) — **done**.
- ICM Phase 1 (distribution modes, conventions, quick reference, release automation) — **done**.
- Eval cases added for prompt design, code review, tool safety, agent handoff, debugging, and orchestrator.
- Model-comparison result template added (`evals/results/_TEMPLATE-model-comparison.md`).
- Run-record examples added under `runs/examples/`.
- Core skill files refined to reference the relevant agent and eval layer.

## v1.1.0 Enhancements (June 2026)

- **GitNexus Code-Cleanup Integration** — Enhanced `/code-cleanup` skill to use explicit
  `gitnexus_impact()` and `gitnexus_detect_changes()` calls instead of generic reference-gating.
  Aligns with CLAUDE.md GitNexus rules for precise blast-radius analysis before code moves.
  HIGH/CRITICAL risk results trigger hard stop. Hybrid approach: GitNexus for code files (call-graph
  analysis), git grep for non-code files (reference counting). See `skills/code-cleanup/`.

## v1.2.0 - 3-Mode Autonomy System (June 19, 2026)

**Release Status:** ✅ Completed

Adds 3 autonomy modes (ask, cautious, full) for controlling approval behavior during orchestrator execution.

### Core Features

- **3 Autonomy Modes:**
  - **Ask:** Approve all operations manually (maximum safety)
  - **Cautious:** Auto-approve LOW/MEDIUM, ask for HIGH, block CRITICAL (balanced, default)
  - **Full:** Auto-approve all operations (trusted automation)

- **Risk Classification:**
  - LOW (0-3 callers): Read, status, query, documentation
  - MEDIUM (4-9 callers): Edit, write, commit, small refactors
  - HIGH (10-24 callers): Delete, push, breaking changes
  - CRITICAL (25+ or critical path): Force operations, production deploys, security boundaries

- **Audit Logging:**
  - JSONL format: `runs/autonomy-decisions.jsonl`
  - Fields: timestamp, mode, operation, risk_level, decision, context
  - Decision types: auto_approved, user_approved, user_rejected, blocked

- **CLI Integration:**
  - `--autonomy {ask|cautious|full}` flag for `scripts/orchestrate.py route --execute`
  - Overrides config default in `configs/autonomy.yaml`

### Implementation

- **Core Module:** `scripts/orchestrator/autonomy_manager.py` (385 lines)
  - AutonomyManager class with mode management, risk classification, approval decision logic
  - GitNexus impact mapping (caller count → risk level)
  - Heuristic fallback when GitNexus unavailable
  - Audit logging with JSONL format

- **Integration:** `scripts/orchestrator/driver.py` (9 additions)
  - Risk classification per step
  - Autonomy gate checks (block/proceed/ask)
  - Summary reporting before audit log save
  - Graceful fallback to legacy gates when autonomy unavailable

- **CLI Support:** `scripts/orchestrate.py` (autonomy_mode parameter)

### Testing & Validation

- **Unit Tests:** `test_autonomy_manager.py` (24 tests, all passing)
  - Mode behavior (ask/cautious/full)
  - Risk classification (file ops, git ops, GitNexus impact)
  - Audit logging (JSONL format, summary accuracy)

- **Integration Tests:** `test_driver_autonomy.py` (7 tests, all passing)
  - Mode integration with execute_route()
  - Audit log creation and format
  - Backward compatibility (no autonomy.yaml)

- **Eval Case:** `evals/cases/autonomy/basic-autonomy-modes.md`
- **Rubric:** `evals/rubrics/autonomy-behavior.md`

### Documentation

- **User Guide:** `docs/AUTONOMY-MODES.md` (comprehensive, 400+ lines)
  - Quick start, mode comparison table
  - Risk levels, audit logging, troubleshooting
  - Best practices, agent-specific guidance

- **Agent Contracts:** Updated builder, planner, reviewer contracts with autonomy guidance
- **Skills:** Updated code-cleanup, commit, validate skills with autonomy recommendations
- **CLAUDE.md:** Added autonomy modes section with quick reference

### Configuration

- **Config File:** `configs/autonomy.yaml` (140 lines)
  - Mode definitions (ask/cautious/full)
  - Risk classifications (file_operations, git_operations, code_changes, gitnexus_impact)
  - Safety guardrails (always_block list)
  - Audit log settings

### Key Design Decisions

1. **CRITICAL risk in cautious mode:** Hard blocked (not just prompted)
2. **Autonomy scope:** Global mode for v1.2.0 (per-route control deferred to v2.0.0)
3. **Audit detail:** Full context in audit log (enables post-execution review)
4. **Backward compatibility:** Works without autonomy.yaml (falls back to legacy gates)

### Files Added/Modified

**Added:**
- `configs/autonomy.yaml`
- `scripts/orchestrator/autonomy_manager.py`
- `scripts/orchestrator/tests/test_autonomy_manager.py`
- `scripts/orchestrator/tests/test_driver_autonomy.py`
- `docs/AUTONOMY-MODES.md`
- `evals/cases/autonomy/basic-autonomy-modes.md`
- `evals/rubrics/autonomy-behavior.md`

**Modified:**
- `scripts/orchestrator/driver.py` (autonomy integration)
- `scripts/orchestrate.py` (CLI flag)
- `agents/*.agent.md` (autonomy guidance)
- `skills/{code-cleanup,commit,validate}/SKILL.md` (autonomy recommendations)
- `CLAUDE.md` (autonomy modes section)

### Dogfooding

v1.2.0 was implemented using the harness's own iteration workflow:
- Planning: AUTOPLAN.md evaluated and approved (5.0/5.0 quality score)
- Implementation: Phased approach (A: Core, B: Integration, C: Docs/Tests)
- Validation: All 31 tests passing (24 unit + 7 integration)
- Documentation: Comprehensive user guide, agent contracts, skills

**Effort:** 14-17.5 hours estimated, actual: ~16 hours (within estimates)

## Completed Milestones

1. ✅ **v1.0.0 Released** (June 16, 2026) — Initial public release with ICM Phase 1 enhancements
2. ✅ **v1.1.0 Released** (June 19, 2026) — GitNexus code-cleanup integration with impact analysis
3. ✅ **v1.2.0 Complete** (June 19, 2026) — 3-mode autonomy system shipped
4. ✅ **Environment Portability** (June 19, 2026) — Multi-environment guides (Cursor, Windsurf, Aider, generic)
5. ✅ **ICM Token Budgets** (June 19, 2026) — All 7 stage CONTEXT.md files enhanced
6. ✅ **Security Baseline** (June 19, 2026) — Comprehensive template with P0/P1/P2 priorities

## Next Steps

1. **Tag v1.2.0** — Create git tag and GitHub release for autonomy system
2. **Real-World Testing** — Validate environment guides with actual Cursor/Windsurf/Aider users
3. **Dogfood** — Apply harness to production applications (bootstrap via `scripts/01-create-project.sh`)
4. **Operate** — Exercise multi-step `--execute` workflows in production
5. **Community Feedback** — Gather user feedback on portability and autonomy modes
6. **Future Enhancements** — Consider: generated JSON config mirrors, stronger execute/resume semantics, additional environment adapters

---

**For detailed version history, see [CHANGELOG.md](./CHANGELOG.md)**
