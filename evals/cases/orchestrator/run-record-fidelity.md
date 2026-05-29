# Eval Case: Run-Record Fidelity

## Purpose

Test whether the orchestrator's run-log writer (Phase 01) emits records that
conform to `telemetry/run-log-schema.md` and match the Markdown-wrapped-YAML
shape of existing `runs/examples/`, and that those records round-trip through
the config reader.

## Input

Generate a run record from a dry-run step, then re-read its embedded YAML block:

```
python3 scripts/orchestrate.py route task_definition --dry-run
# then re-parse the emitted runs/<run-id>.md YAML block via config.load_yaml
```

## Expected Qualities

- Output is a `.md` file containing a fenced ```yaml block, matching `runs/examples/` style.
- All required schema fields are present: `run_id`, `created_at`, `request`, `agent`, plus `validation.status`.
- `agent` is one of `planner|builder|reviewer|researcher|evaluator`.
- `validation.status` is one of `passed|failed|skipped` (`skipped` for dry-run).
- `run_id` is `YYYYMMDD-HHMMSS-short-name`; no filename collisions across steps (timestamped/unique).
- `inputs`/`outputs` are lists of repo-root-relative paths or descriptions.
- The embedded YAML re-parses cleanly via the Phase 01 reader (round-trip integrity).

## Rubric

Use `evals/rubrics/orchestrator-output-quality.md`. Run-record schema
conformance must score 4 or higher to pass (correctness-critical).
