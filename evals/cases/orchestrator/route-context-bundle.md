# Eval Case: Route Context-Bundle Assembly

## Purpose

Test whether the orchestrator's sequencer (Phase 02) can resolve a lifecycle
route into ordered, contract-backed steps and assemble a complete context bundle
for each step — in dry-run, with no model invocation.

## Input

Run the sequencer over the `iteration` route from `configs/routing.yaml` (the
richest route: `planner → builder → evaluator`):

```
python3 scripts/orchestrate.py route iteration --dry-run
```

## Expected Qualities

- Produces exactly three ordered steps (planner, builder, evaluator), matching list order in `routing.yaml`.
- Each step resolves to its contract (`agents/*.agent.md`), `default_skill`, and `model_profile` from `configs/agents.yaml`.
- Each bundle references a prompt version (`prompts/<agent>/v1.md`) and the declared stage inputs.
- A dry-run run record is written per step, `validation.status: skipped`, conforming to `telemetry/run-log-schema.md`.
- All paths in output and records are repo-root-relative.
- No model/network call occurs; no dependency is installed.

## Rubric

Use `evals/rubrics/orchestrator-output-quality.md`.
