# Orchestrator Dogfood + Error-Handling Verification

**Date:** 2026-05-30  
**Rubric:** `evals/rubrics/orchestrator-output-quality.md`  
**Verdict:** PASS (operational checks)

## Harness baseline

```text
scripts/07-validate-harness.sh:  Passed 98 | Warnings 0 | Failed 0
Orchestrator unit tests:         70 passed (repo root)
```

## Error-handling cases

| Case | Check | Result |
|------|-------|--------|
| `invalid-route.md` | `route nonexistent_route` | PASS — exit 2, lists valid routes from `routing.yaml` |
| `missing-references.md` | Unit: `test_missing_refs_reported_not_skipped` | PASS — missing paths in `bundle.missing`, surfaced as run issues |
| `malformed-config.md` | Unit: config reader rejects bad YAML | PASS — covered in `test_config.py` |
| `phase-04-timeout-handling.md` | Unit: `test_timeout_is_failed_with_note` | PASS |
| `phase-04-execute-real-cli.md` | `route task_definition --execute --max-steps 1 --yes` | PASS — see `20260529-orchestrator-phase-04-execute-uat.md` |

## Dogfood workflow

| Step | Command | Result |
|------|---------|--------|
| Full route dry-run | `route iteration --dry-run` | PASS — 3 step records under `runs/20260530-055914-iteration-*.md` |
| Single-step execute | `route iteration --execute --adapter cli --max-steps 1 --yes` | PASS — `runs/20260530-055918-iteration-01-planner.md`, stdout captured |

**Config:** `configs/execution.yaml` → `claude -p`, `env_allowlist` for API keys, `timeout_seconds: 300`.

## Notes

- Execute step latency ~2–3 min per step with `claude -p`; use `--max-steps` to bound cost.
- Default adapter remains `noop`; dry-run is still the safe default for CI and templates.
- Next milestone: bootstrap harness onto a **target application repo** and run `task_definition` → `iteration` on real work.
