# Effort: Native Orchestrator

A dependency-free run driver owned entirely by the harness. **Implemented — Phases 01–04 built** in `scripts/orchestrator/` + `scripts/orchestrate.py`: a dry-run coordinator by default, with opt-in `--execute` added in Phase 04. Phases 01–03 passed the orchestrator-output-quality eval at 5.0/5.0 (see *Run + Eval Links*).

## Goal

Give the harness its own optional, plain-text-driven engine that can sequence agents through the lifecycle and record runs — with zero third-party dependencies and no reliance on any external framework.

## Why

The harness is currently agent-driven: a human or AI assistant follows `configs/routing.yaml` and stage contracts by hand. That is correct and sufficient for assisted work, but complex, multi-phase development benefits from a driver that:

- Reads `configs/agents.yaml` + `configs/routing.yaml` and computes the intended agent/stage sequence.
- Loads the right contract, skill procedure, prompt version, and model profile for each step.
- Emits a run record per `telemetry/run-log-schema.md` for every step.
- Stays a thin coordinator — it never replaces the reasoning agent; it assembles context and records what happened.

## Scope

- In scope: a local CLI that resolves config, sequences steps, assembles per-step context bundles, and writes run records. Dry-run by default.
- Out of scope **for the dry-run core (01–03)**: calling model providers/APIs directly, autonomous decision-making, networked execution, any package dependency. Model invocation is the core's *output* (a prepared context bundle). **Phase 04 (now built)** is the opt-in, approval-gated adapter that executes that bundle — see *Autonomy boundary*. It never runs by default and adds no pip dependency (it shells out to an already-installed CLI).

## Design Decisions

### Language: Python (standard library only)

Chosen over Bash because the orchestrator needs state, structured data, and run-log emission that Bash handles poorly. Constraints:

- Python 3.9+ standard library only. **No PyYAML or other packages.**
- YAML config stays the human-facing source of truth. The orchestrator includes a compact, stdlib-only reader for the **indentation-based YAML subset** these configs and run records use (nested mappings, lists of scalars and of mappings, scalars, `#` comments, `null`) — defined in `01-config-and-runlog.md`. If configs ever outgrow that subset, the fallback is to emit a generated `configs/*.generated.json` via a build step — still dependency-free.
- Run records are written as Markdown-wrapped YAML (matching existing `runs/` examples) using string templates, not a YAML library.

### Paths are always relative to a detected repo root

The orchestrator must never hardcode or persist absolute, machine-specific paths. It detects the repo root the same way the existing scripts do — from the script's own location (`BASH_SOURCE`/`__file__`) or a `PROJECT_ROOT` override — and resolves every config, contract, prompt, run, and eval path relative to that root. Generated state and run records store repo-relative paths only. (This mirrors `scripts/07-validate-harness.sh`'s `ROOT` handling and avoids the committed-absolute-path problem fixed in `scripts/.icm-project-path`.)

### Coordinator, not executor

The driver prepares a **context bundle** per step (contract + procedure + prompt + inputs + model profile) and records intent/outcome. It does not itself reason or call an LLM. This preserves the "agent-driven" model while automating the bookkeeping that is error-prone by hand.

### Autonomy boundary: 01–03 coordinate, 04 (opt-in) executes

The Goal and Scope above describe the **core (phases 01–03)**: dependency-free, dry-run, no model/network calls. That core automates *clerical* work — which agent/stage is next, loading the right contract/prompt/profile, writing run records — but never the *reasoning or execution* of a step. A clean build of 01–03 therefore yields automated bookkeeping, **not** autonomous app-building.

**Phase 04 (Execution Adapter)** is the single, opt-in exception that crosses the coordinator→executor line. It is the only component permitted an external runtime dependency and model/network access, it wraps an existing agent runtime rather than building a bespoke model client (so the harness stays backend-agnostic), and it is never the default — gated behind an explicit `--execute` flag. The core's purity guarantees stay intact for 01–03; all dependency/network behavior is quarantined in 04. Even with 04, the autonomy ceiling is the checkpoint policy in `configs/tools.yaml` + `CLAUDE.md` (commits, installs, destructive ops still need human approval) — "minimal intervention" by design, not zero.

## Phases

| # | Phase | Plan File | Depends On | Status |
|---|-------|-----------|------------|--------|
| 01 | Config loader + run-log writer | `01-config-and-runlog.md` | — | done |
| 02 | Stage/agent sequencer (dry-run) | `02-sequencer.md` | 01 | done |
| 03 | CLI + eval hook | `03-cli-and-eval-hook.md` | 02 | done |
| 04 | Execution adapter (opt-in) | `04-execution-adapter.md` | 03 | done |

Status values: `todo`, `doing`, `review`, `done`.

Phases 01–03 are the dependency-free, dry-run core. Phase 04 is the opt-in executor described in *Autonomy boundary* above — it intentionally steps outside the core's no-deps/dry-run guarantees and has its own validation in its plan.

## Dependency Order

```text
01 → 02 → 03 → 04 (opt-in)
```

## Validation

- [x] Each phase plan reviewed (plan-quality pass over 01–04)
- [x] `scripts/07-validate-harness.sh` passes (93/93)
- [x] Orchestrator runs with `python3` and no `pip install` step
- [x] A dry-run produces a valid run record under `runs/`
- [x] Eval cases in `evals/cases/` can be invoked through the CLI
- [x] 69 unit tests pass (`python3 -m unittest discover -t . -s scripts/orchestrator`)

## Run + Eval Links

- Runs: dry-run records under `runs/` (e.g. `runs/20260529-*-<route>-<step>-<agent>.md`); execute-mode adds real per-step records plus captured stdout/stderr.
- Evals: `evals/results/20260529-orchestrator-phase-01-03-validation.md` — Phases 01–03 PASS, 5.0/5.0. Phase 04 `--execute` UAT: `evals/results/20260529-orchestrator-phase-04-execute-uat.md` (stub CLI configured in `configs/execution.yaml`).

## Open Questions

- ~~Should the orchestrator live in `scripts/` or a new top-level `orchestrator/` folder?~~ **Resolved:** package at `scripts/orchestrator/` with entry `scripts/orchestrate.py`. Import strategy is locked in `01-config-and-runlog.md` → *Package & Import Convention*.
- Is the flat-YAML-subset reader acceptable long-term, or should configs gain generated JSON mirrors for robustness?
