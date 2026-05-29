# AI Agent Development Harness

A plain-text, model-agnostic harness for designing, evaluating, and improving AI agents and model workflows.

This repository evolved from an ICM workspace template into an agent/model development harness. It keeps the strengths of staged context, reusable skills, and human checkpoints while adding first-class support for agents, prompts, model profiles, evals, run records, and tool safety policies.

## What This Is (and Is Not)

This is a **context and methodology harness**, not a runtime engine.

- It provides explicit, inspectable contracts (agents, skills, prompts, configs, evals, stages) that a **capable AI agent or a human drives**.
- It does **not** ship an orchestrator, scheduler, or autonomous multi-agent runtime. Handoffs, routing, and sequencing are followed by whoever drives the work, guided by `configs/routing.yaml` and the stage contracts.
- It is fully **self-contained and dependency-free**: every artifact is plain text, and `scripts/07-validate-harness.sh` validates structure and cross-references with no external tooling.

A native, dependency-free orchestrator is specified (not yet built) under `plans/native-orchestrator/`.

## Start Here

1. Read `CLAUDE.md` for assistant operating instructions.
2. Read `FRAMEWORK.md` for the conceptual model.
3. Use `CONTEXT.md` to route work to the correct lifecycle stage.
4. Use `agents/`, `skills/`, `prompts/`, `models/`, `configs/`, and `evals/` as the core framework layers.

## Core Lifecycle

```text
Task Definition → Agent Design → Prompt Design → Tool Integration → Evaluation → Iteration → Release
```

## Key Folders

| Folder | Purpose |
|--------|---------|
| `agents/` | Agent contracts with roles, permissions, outputs, and handoffs |
| `skills/` | Reusable command/workflow procedures |
| `prompts/` | Versioned prompt templates and changelogs |
| `plans/` | Implementation-ready plans and multi-phase efforts |
| `models/` | Provider guidance and model comparison notes |
| `configs/` | YAML profiles for agents, models, routing, and tools |
| `evals/` | Rubrics, eval cases, and results |
| `stages/` | Lifecycle stage contracts |
| `runs/` | Execution records and experiment notes |
| `telemetry/` | Run-log schema and observability guidance |
| `scripts/` | Bootstrap and validation utilities |

## Recommended Workflow

For new or changed agent/model behavior:

1. Define the task in `stages/01-task-definition/`.
2. Create or update the agent contract in `agents/`.
3. Create or update prompts in `prompts/`.
4. Confirm tool permissions in `configs/tools.yaml`.
5. Evaluate with `evals/rubrics/` and `evals/cases/`.
6. Iterate based on findings.
7. Release with documented validation and safe commit review.

## Safety Principles

- Keep destructive actions behind explicit approval.
- Do not read secrets unnecessarily.
- Do not install dependencies without approval.
- Do not stage or commit without approval.
- Treat evaluation failures as useful evidence, not something to hide.
