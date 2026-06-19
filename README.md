# AI Agent Development Harness

A plain-text, model-agnostic harness for designing, evaluating, and improving AI agents and model workflows.

**✨ Works with Multiple Environments:** Use with Cursor, Windsurf, Aider, or any AI coding environment.
📖 **See:** [Environment Adaptation Guides](./docs/adapters/) for setup instructions.

**📋 Version History:** See [CHANGELOG.md](./CHANGELOG.md) for release notes and upgrade guides.

This repository evolved from an ICM workspace template into an agent/model development harness. It keeps the strengths of staged context, reusable skills, and human checkpoints while adding first-class support for agents, prompts, model profiles, evals, run records, and tool safety policies.

## What This Is (and Is Not)

This is a **context and methodology harness**, not a runtime engine.

- It provides explicit, inspectable contracts (agents, skills, prompts, configs, evals, stages) that a **capable AI agent or a human drives**.
- It does **not** ship an autonomous multi-agent runtime. There is now an optional, dependency-free orchestrator CLI (`scripts/orchestrate.py`) that *coordinates* — it computes the route/stage sequence and assembles per-step context bundles in dry-run — but it does not reason or call a model. Handoffs and sequencing are still driven by whoever runs the work, guided by `configs/routing.yaml` and the stage contracts.
- It is fully **self-contained and dependency-free**: every artifact is plain text, and `scripts/07-validate-harness.sh` validates structure and cross-references with no external tooling.

The native orchestrator's dry-run core is implemented under `plans/native-orchestrator/`: config reader + run-log writer (Phase 01), stage/agent sequencer (Phase 02), and the CLI + eval hook (Phase 03), all in `scripts/orchestrator/` and `scripts/orchestrate.py`. It remains a coordinator, never an executor; the opt-in execution adapter is Phase 04.

## Use This Harness

This repo is a **template**, not a library you install. Pick one:

| Goal | How |
|------|-----|
| New project from GitHub | **Use this template** on GitHub → clone → customize `_config/project-notes.md` |
| Local scaffold | `scripts/01-create-project.sh` (add `--with-orchestrator` for the CLI) |
| Attach to an existing app | Bootstrap into a subfolder (e.g. `harness/`) — see `DISTRIBUTION.md` |

Full paths, trimming optional features, and maintainer release steps: **`DISTRIBUTION.md`**.

**First time?** Walk through **`TUTORIAL.md`** — new project, existing project, and a full lifecycle example.

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

A dependency-free coordinator (stdlib Python; no install), dry-run by default with opt-in execution. Implemented in Phases 01-04 of `plans/native-orchestrator/`.

### What It Does

- **Phase 01**: Reads `configs/*.yaml` with a stdlib-only YAML subset parser; writes run records conforming to `telemetry/run-log-schema.md`
- **Phase 02**: Resolves lifecycle routes from `configs/routing.yaml` into ordered agent steps with context bundles
- **Phase 03**: Provides CLI + eval scaffolding hooks
- **Phase 04**: Adds opt-in, approval-gated execution (`route --execute`) via pluggable adapters (`noop`/`cli`)

### Usage

Run from the repo root:

```bash
# Sequence a lifecycle route into per-step context bundles (dry-run)
python3 scripts/orchestrate.py route <route-name>

# Pair an eval case with its rubric and scaffold a PENDING result + run record
python3 scripts/orchestrate.py eval evals/cases/<category>/<case>.md

# Opt-in: run a route step-by-step through an adapter (approval-gated)
python3 scripts/orchestrate.py route <route-name> --execute --adapter cli --max-steps 1
```

### Available Routes

Defined in `configs/routing.yaml`:

| Route | Stage | Agents |
|-------|-------|--------|
| `task_definition` | 01-task-definition | researcher → planner |
| `agent_design` | 02-agent-design | planner → reviewer |
| `prompt_design` | 03-prompt-design | planner → reviewer |
| `tool_integration` | 04-tool-integration | builder → reviewer |
| `evaluation` | 05-evaluation | evaluator → reviewer |
| `iteration` | 06-iteration | planner → builder → evaluator |
| `release` | 07-release | reviewer |

### Output

- **Run records**: Written to `runs/YYYYMMDD-HHMMSS-<route>-<step>-<agent>.md`
- **Format**: Markdown-wrapped YAML conforming to `telemetry/run-log-schema.md`
- **Validation**: All Phase 01-03 output scored 5/5 across 8 criteria in `evals/results/20260529-orchestrator-phase-01-03-validation.md`

### Safety Model

The orchestrator is **coordinator-first** by design:

- Dry-run by default; execution is **opt-in and approval-gated** via `--execute`
- The default path never invokes a model or makes network calls
- Assembles context bundles and records intent; only `--execute` runs a step (through an adapter)
- Dependency-free: Python 3.9+ stdlib only, no `pip install` (the `cli` adapter shells out to an *already-installed* CLI)

**Phase 04** (execution adapter) is implemented: `route --execute` runs each step through an adapter — `noop` (default; assembles but executes nothing) or `cli` (shells out to the agent CLI configured in `configs/execution.yaml`). It stays opt-in and approval-gated: `configs/tools.yaml` gates and the self-modification guard (writes to `agents/`, `configs/`, `scripts/orchestrator/`) are **never** waived by `--yes`, `--max-steps` bounds the loop, and the adapter never commits or installs autonomously. See `plans/native-orchestrator/04-execution-adapter.md`.

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

## Version History

See [CHANGELOG.md](./CHANGELOG.md) for:
- Release notes for v1.0.0 (initial release), v1.1.0 (GitNexus integration), v1.2.0 (3-mode autonomy)
- Upgrade guides and migration notes
- Full changelog following [keepachangelog.com](https://keepachangelog.com/) format
