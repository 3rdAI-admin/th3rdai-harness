# Effort: <Effort Name>

Template for a multi-phase effort. Copy this folder to `plans/<effort-name>/` and fill it in.

## Goal

<one-sentence objective for the whole effort>

## Scope

- In scope: <what this effort covers>
- Out of scope: <what it intentionally avoids>

## Phases

Each phase has its own plan file (use the template in `skills/plan/planner.md`).

| # | Phase | Plan File | Depends On | Status |
|---|-------|-----------|------------|--------|
| 01 | <phase name> | `01-<phase>.md` | — | todo |
| 02 | <phase name> | `02-<phase>.md` | 01 | todo |

Status values: `todo`, `doing`, `review`, `done`.

## Dependency Order

The harness has no scheduler. This is the order an agent or human must follow:

```text
01 → 02 → ...
```

Phases with no dependency on each other may run in any order or in parallel by separate agents.

## Validation

- [ ] Each phase plan passes `/plan-reviewer`
- [ ] `scripts/07-validate-harness.sh` passes after each phase
- [ ] Run records linked in `runs/` for executed phases
- [ ] Eval results linked in `evals/results/` where behavior changed

## Run + Eval Links

- Runs: <runs/... once executed>
- Evals: <evals/results/... once evaluated>

## Open Questions

- <question or none>
