# Effort: Native Orchestrator

Specification for a dependency-free run driver owned entirely by the harness. **Spec only — not yet built.** This effort defines what to build; execution happens after review.

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
- Out of scope: calling model providers/APIs directly, autonomous decision-making, networked execution, any package dependency. Model invocation remains the driver's *output* (a prepared context bundle) that a human/agent or a future adapter executes.

## Design Decisions

### Language: Python (standard library only)

Chosen over Bash because the orchestrator needs state, structured data, and run-log emission that Bash handles poorly. Constraints:

- Python 3.9+ standard library only. **No PyYAML or other packages.**
- YAML config stays the human-facing source of truth. The orchestrator includes a small (~60-line) stdlib-only reader for the **flat YAML subset** these configs use (mappings, lists, scalars, comments). If configs ever outgrow that subset, the fallback is to emit a generated `configs/*.generated.json` via a build step — still dependency-free.
- Run records are written as Markdown-wrapped YAML (matching existing `runs/` examples) using string templates, not a YAML library.

### Coordinator, not executor

The driver prepares a **context bundle** per step (contract + procedure + prompt + inputs + model profile) and records intent/outcome. It does not itself reason or call an LLM. This preserves the "agent-driven" model while automating the bookkeeping that is error-prone by hand.

## Phases

| # | Phase | Plan File | Depends On | Status |
|---|-------|-----------|------------|--------|
| 01 | Config loader + run-log writer | `01-config-and-runlog.md` | — | todo |
| 02 | Stage/agent sequencer (dry-run) | `02-sequencer.md` | 01 | todo |
| 03 | CLI + eval hook | `03-cli-and-eval-hook.md` | 02 | todo |

Status values: `todo`, `doing`, `review`, `done`.

## Dependency Order

```text
01 → 02 → 03
```

## Validation

- [ ] Each phase plan passes `/plan-reviewer`
- [ ] `scripts/07-validate-harness.sh` passes after each phase
- [ ] Orchestrator runs with `python3` and no `pip install` step
- [ ] A dry-run produces a valid run record under `runs/`
- [ ] Eval cases in `evals/cases/` can be invoked through the CLI

## Run + Eval Links

- Runs: <runs/... once executed>
- Evals: <evals/results/... once evaluated>

## Open Questions

- Should the orchestrator live in `scripts/` (alongside validation) or a new `orchestrator/` top-level folder? Leaning `scripts/orchestrate.py` to avoid adding a layer.
- Is the flat-YAML-subset reader acceptable long-term, or should configs gain generated JSON mirrors for robustness?
