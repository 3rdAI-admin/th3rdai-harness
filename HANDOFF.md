# Project Handoff

## Last Updated

**May 29, 2026** — Native Orchestrator Phases 01–04 **implemented and validated**. Phases 01–03 PASS 5.0/5.0 (`evals/results/20260529-orchestrator-phase-01-03-validation.md`). Phase 04 PASS all 7 spec criteria, 26/26 tests (`evals/results/20260529-orchestrator-phase-04-validation.md`). Status: 01–03 done, 04 review (awaiting human verification with real CLI). Harness validator **93/93**; orchestrator tests **69/69**.

---

## Resume Here (next session)

Read in order: this file → `README.md` (orchestrator CLI section) → `VERSION3.md` → `plans/native-orchestrator/EFFORT.md`.

**Verify green:** see `_config/project-notes.md` (this repo) or:

```bash
scripts/07-validate-harness.sh
python3 -m unittest discover scripts/orchestrator/tests
```

**Try the orchestrator:**

```bash
python3 scripts/orchestrate.py --help
python3 scripts/orchestrate.py route task_definition --dry-run
python3 scripts/orchestrate.py eval evals/cases/orchestrator/config-subset-parsing.md
```

**Pick up in priority order:**

1. **Human verification required** — Configure real agent CLI in `configs/execution.yaml` `cli.command` (e.g. `["claude", "-p"]`), test --execute flag end-to-end (see Archon task #110), then promote Phase 04 from 'review' to 'done' in EFFORT.md
2. **Optional** — Add orchestrator error-handling eval cases; formal eval case for Phase 04 cli-execute with real CLI
3. **Optional** — Commit uncommitted run records and skill updates (requires user approval per CLAUDE.md)

**Do not assume** the harness autonomously builds apps without an external agent/CLI — even with Phase 04, it coordinates and optionally shells out; commits and destructive actions still require human approval per `configs/tools.yaml` and `CLAUDE.md`.

---

## Session Summary — May 28–29, 2026

### Harness alignment (May 28)

- Stage contracts `01`–`03` rewritten (Task Definition / Agent Design / Prompt Design); legacy material under `archive/`.
- Eval cases, run examples, skill refinements (plan-reviewer, e2e-test, gitcommit), model-comparison template.
- Git repo + `.gitignore`; plan skill renamed to `skills/plan/planner.md`.

### Native Orchestrator (May 28–29)

| Phase | Deliverable | Status |
|-------|-------------|--------|
| 01 | `scripts/orchestrator/config.py`, `runlog.py` — stdlib YAML reader + run-record writer | **done** |
| 02 | `scripts/orchestrator/sequencer.py` — route → context bundles + dry-run records | **done** |
| 03 | `scripts/orchestrate.py`, `evalhook.py` — CLI `route` + `eval` subcommands | **done** |
| 04 | `adapter.py`, `gates.py`, `configs/execution.yaml` — opt-in `--execute` | **review** (validated 26/26 tests; awaiting human verification) |

- Import convention locked: `from scripts.orchestrator import ...` (tests pass from repo root).
- Phase 04 spec: `plans/native-orchestrator/04-execution-adapter.md`.
- Effort tracker: `plans/native-orchestrator/EFFORT.md`.

### Eval layer

- Rubric: `evals/rubrics/orchestrator-output-quality.md`.
- Cases: `evals/cases/orchestrator/{config-subset-parsing,run-record-fidelity,route-context-bundle}.md`.
- Validator enforces case ↔ rubric coherence (93 checks total).
- Formal result: `evals/results/20260529-orchestrator-phase-01-03-validation.md` — **PASS**, 8/8 criteria at 5.0.
- Registry tables in `evals/README.md`.

### Docs

- `VERSION3.md` updated — orchestrator section, full eval inventory, completed vs live next steps.
- `README.md` updated — orchestrator CLI usage, Phase 04 framing.

### Tracking

- **Archon:** project **Th3rdai-Harness** (`eb8b4363-b1f0-4448-8e71-c557e0daa5b2`). Native Orchestrator milestone complete (20/20 tasks done). Open: human verification of Phase 04 with real CLI (task #110), optional docs/skills commit (task #50).

---

## Current State

Plain-text, model-agnostic **AI Agent Development Harness** — not a deployable app. It provides agents, skills, prompts, model profiles, configs, evals, runs, telemetry, and seven lifecycle stages for designing and improving agent workflows.

**New since May 28:** an optional **Native Orchestrator** (`scripts/orchestrate.py`) that automates route sequencing, context-bundle assembly, and run logging. Dry-run by default; opt-in execution via Phase 04.

Framework layers: Agents · Skills · Prompts · Models · Configs · Evals · Runs · Telemetry · Lifecycle stages.

Lifecycle:

```text
01-task-definition → 02-agent-design → 03-prompt-design → 04-tool-integration
  → 05-evaluation → 06-iteration → 07-release
```

---

## Key Files to Read First

| Priority | File | Why |
|----------|------|-----|
| 1 | `README.md` | Overview + orchestrator CLI |
| 2 | `VERSION3.md` | Alignment plan + orchestrator phase table |
| 3 | `HANDOFF.md` | This file |
| 4 | `FRAMEWORK.md` | Conceptual model |
| 5 | `CLAUDE.md` | Assistant rules (commits need approval) |
| 6 | `CONTEXT.md` | Stage routing |
| 7 | `plans/native-orchestrator/EFFORT.md` | Orchestrator effort status |
| 8 | `configs/routing.yaml` | Route names for `orchestrate route` |
| 9 | `evals/results/20260529-orchestrator-phase-01-03-validation.md` | Latest formal eval |
| 10 | `scripts/07-validate-harness.sh` | Structural gate |

---

## Native Orchestrator Quick Reference

**Package:** `scripts/orchestrator/` · **CLI:** `scripts/orchestrate.py` · **Plans:** `plans/native-orchestrator/`

```bash
# Dry-run a lifecycle route (writes run records under runs/)
python3 scripts/orchestrate.py route <route-name> --dry-run

# Routes: task_definition, agent_design, prompt_design, tool_integration,
#         evaluation, iteration, release  (from configs/routing.yaml)

# Scaffold an eval result from a case + rubric
python3 scripts/orchestrate.py eval evals/cases/orchestrator/<case>.md

# Opt-in execution (Phase 04) — requires configs/execution.yaml cli.command
python3 scripts/orchestrate.py route <route-name> --execute --adapter cli --max-steps 1
```

**Design constraints:** stdlib only (no `pip install`); repo-root-relative paths; coordinator-first; approval gates from `configs/tools.yaml` are never waived by `--yes`.

---

## Validation (current)

```bash
bash -n scripts/*.sh
scripts/07-validate-harness.sh
python3 -m unittest discover scripts/orchestrator/tests
```

Latest results:

```text
Harness validator:  Passed 93 | Warnings 0 | Failed 0
Orchestrator tests: 69 passed (from repo root)
```

---

## Evaluation Assets (current)

**Rubrics:** `plan-quality`, `tool-safety`, `agent-output-quality`, `orchestrator-output-quality`

**Cases:** `planning/`, `prompt-design/`, `code-review/`, `agent-handoff/`, `debugging/`, `tool-safety/`, `orchestrator/` (3 cases)

**Results:** `evals/results/_TEMPLATE-model-comparison.md`, `evals/results/20260529-orchestrator-phase-01-03-validation.md`, `evals/results/20260529-orchestrator-phase-04-validation.md`

**Examples:** `runs/examples/`, plus live dry-run records under `runs/20260529-*.md`

---

## Important Notes

- **Git repo** with baseline commit; **no commits without explicit human approval** (`CLAUDE.md`).
- **Archon** tracks work — check **Th3rdai-Harness** before coding; update task status when resuming.
- **GitNexus** indexed — run `npx gitnexus analyze` after structural changes; use impact analysis before editing symbols.
- Plan skill: `skills/plan/planner.md` (not `plan.md`). Reviewer: `skills/plan/plan-reviewer.md`.
- Legacy ICM material: `archive/legacy-docs/`, `archive/legacy-stage-outputs/`.
- **Uncommitted work likely** — check `git status` before assuming a clean tree.

---

## Historical Context (May 25–28)

Earlier sessions aligned bootstrap scripts (`01`–`07`), agent contracts, skills, prompts, configs, stage contracts, eval baseline, and archived PRP-era docs. That work is **complete** unless validation regresses. Details remain in git history and Archon completed tasks; do not re-do unless files were reverted.

May 28 validator was **47/47**; grew to **93/93** after eval coherence checks and orchestrator rubric registration.

---

## Suggested Next Agent Prompt

```text
You are resuming the AI Agent Development Harness (th3rdai-harness). Read HANDOFF.md first, then README.md, VERSION3.md, and plans/native-orchestrator/EFFORT.md.

State: Native Orchestrator ALL 4 PHASES COMPLETE AND VALIDATED. Phases 01–03 PASS 5.0/5.0 (evals/results/20260529-orchestrator-phase-01-03-validation.md). Phase 04 PASS all 7 spec criteria, 26/26 tests (evals/results/20260529-orchestrator-phase-04-validation.md). Status in EFFORT.md: 01–03 done, 04 review. Documentation synced (commit 9871ad4). configs/execution.yaml has empty cli.command (safe default). Harness validator: 93/93. Orchestrator tests: 69/69.

Immediate next step: Human verification of Phase 04 with real CLI command (Archon task #110). Configure configs/execution.yaml cli.command to a real agent CLI (e.g., ["claude", "-p"]), test --execute flag end-to-end, verify 8 checkpoints listed in task, then promote Phase 04 to 'done' in EFFORT.md.

Run scripts/07-validate-harness.sh before and after changes. Do not commit without explicit approval. Update Archon (Th3rdai-Harness) when tasks complete.
```
