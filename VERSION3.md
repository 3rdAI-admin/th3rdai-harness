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

Initial eval assets:

- `evals/rubrics/plan-quality.md`
- `evals/rubrics/tool-safety.md`
- `evals/rubrics/agent-output-quality.md`
- `evals/cases/planning/basic-feature-plan.md`

### 7. Runs and Telemetry

**Folders:** `runs/`, `telemetry/`

Runs record execution history. Telemetry defines run-log conventions and observability guidance.

Use `telemetry/run-log-schema.md` when recording agent, prompt, model, or eval runs.

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

## Safety Principles

- Keep destructive actions behind explicit approval.
- Do not read secrets unnecessarily.
- Do not install dependencies without approval.
- Do not stage or commit without approval.
- Record skipped validation honestly.
- Treat eval failures as evidence for iteration.

## Next Steps

1. Update older bootstrap scripts to generate the full agent harness structure by default.
2. Add more eval cases for debugging, refactoring, prompt design, and code review.
3. Add model comparison result templates.
4. Add run-record examples under `runs/`.
5. Continue refining skill files so each one references the relevant agent and eval layer.
