# Runs

Recorded executions of agents, skills, prompts, and evaluations. Each run answers *what happened, with which inputs, model, outputs, and results?*

## Conventions

- One file per run, named `<run-id>.md` where `run_id` is `YYYYMMDD-HHMMSS-short-name`.
- Each run conforms to `telemetry/run-log-schema.md`.
- Reusable or illustrative runs live under `runs/examples/`.
- Evaluation runs also write a result to `evals/results/`.

## How to Add a Run

1. Copy the schema from `telemetry/run-log-schema.md`.
2. Fill in agent, skill, prompt version, model profile, inputs, outputs, validation, and findings.
3. Record failures honestly — failed runs are evidence, not something to hide.
4. Save as `runs/<run-id>.md` (or `runs/examples/<run-id>.md` for reference runs).

## Index

| Run | Agent | Type | Result |
|-----|-------|------|--------|
| `examples/20260528-101500-health-endpoint-plan.md` | Planner | Plan creation | Passed; handoff to Builder |
| `examples/20260528-103000-health-plan-eval.md` | Evaluator | Plan evaluation | Scored against `plan-quality` rubric |

Update this table when adding a run that others should be able to find.
