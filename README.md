# AI Agent Development Harness

A plain-text, model-agnostic harness for designing, evaluating, and improving AI agents and model workflows.

This repository evolved from an ICM workspace template into an agent/model development harness. It keeps the strengths of staged context, reusable skills, and human checkpoints while adding first-class support for agents, prompts, model profiles, evals, run records, and tool safety policies.

## What This Is (and Is Not)

This is a **context and methodology harness**, not a runtime engine.

- It provides explicit, inspectable contracts (agents, skills, prompts, configs, evals, stages) that a **capable AI agent or a human drives**.
- It does **not** ship an autonomous multi-agent runtime. There is now an optional, dependency-free orchestrator CLI (`scripts/orchestrate.py`) that *coordinates* — it computes the route/stage sequence and assembles per-step context bundles in dry-run — but it does not reason or call a model. Handoffs and sequencing are still driven by whoever runs the work, guided by `configs/routing.yaml` and the stage contracts.
- It is fully **self-contained and dependency-free**: every artifact is plain text, and `scripts/07-validate-harness.sh` validates structure and cross-references with no external tooling.

The native orchestrator's dry-run core is implemented under `plans/native-orchestrator/`: config reader + run-log writer (Phase 01), stage/agent sequencer (Phase 02), and the CLI + eval hook (Phase 03), all in `scripts/orchestrator/` and `scripts/orchestrate.py`. It remains a coordinator, never an executor; the opt-in execution adapter is Phase 04.

## Start Here

1. Read `CLAUDE.md` for assistant operating instructions.
2. Read `FRAMEWORK.md` for the conceptual model.
3. Use `CONTEXT.md` to route work to the correct lifecycle stage.
4. Use `agents/`, `skills/`, `prompts/`, `models/`, `configs/`, and `evals/` as the core framework layers.

## Core Lifecycle

```text
Task Definition → Agent Design → Prompt Design → Tool Integration → Evaluation → Iteration → Release
```

## Optional Orchestrator CLI

A dependency-free, dry-run coordinator (stdlib Python; no install). Run from the repo root:

```text
# Sequence a lifecycle route into per-step context bundles (dry-run)
python3 scripts/orchestrate.py route iteration

# Pair an eval case with its rubric and scaffold a PENDING result + run record
python3 scripts/orchestrate.py eval evals/cases/planning/basic-feature-plan.md
```

It never invokes a model or network — it assembles context and records runs. The opt-in `--execute` mode is specified for Phase 04.

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
