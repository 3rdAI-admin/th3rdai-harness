# AI Agent Development Harness Alignment Plan - Version 3

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
(UAT stub by default; swap in a real agent CLI when ready). `--execute` honors
`configs/tools.yaml` approval gates, performs no autonomous commits, and forbids
self-modification without approval. UAT: `evals/results/20260529-orchestrator-phase-04-execute-uat.md`.

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
scripts/07-validate-harness.sh
```

This checks structure, cross-references (agent ↔ skill ↔ prompt ↔ config ↔
model profile), stage-contract coherence, skill path resolution, and eval
case ↔ rubric coherence. The Native Orchestrator additionally has stdlib unit
tests under `scripts/orchestrator/tests/` (run from `scripts/`:
`python3 -m unittest discover -s orchestrator/tests`).

## Safety Principles

- Keep destructive actions behind explicit approval.
- Do not read secrets unnecessarily.
- Do not install dependencies without approval.
- Do not stage or commit without approval.
- Record skipped validation honestly.
- Treat eval failures as evidence for iteration.

## Completed (earlier milestones)

The following were completed and are no longer pending:

- Bootstrap scripts (`scripts/01`–`07`) generate the full agent harness structure by default.
- Eval cases added for prompt design, code review, tool safety, agent handoff, and debugging.
- Model-comparison result template added (`evals/results/_TEMPLATE-model-comparison.md`).
- Run-record examples added under `runs/examples/`.
- Core skill files refined to reference the relevant agent and eval layer.

## Next Steps

1. Optional: replace `configs/execution.yaml` UAT stub with a real agent CLI (e.g. `claude -p`).
2. Continue expanding eval cases and run records as workflows mature.
3. Use the orchestrator in real development flows and record outcomes under `runs/` and `evals/results/`.
