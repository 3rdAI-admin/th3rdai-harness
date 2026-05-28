# Model Comparison Result — TEMPLATE

Copy this file to `evals/results/<YYYYMMDD>-<case>-comparison.md` and fill it in. Run the same eval case across each model profile without changing the rubric mid-run.

## Setup

| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Eval case | `evals/cases/<category>/<case>.md` |
| Rubric | `evals/rubrics/<rubric>.md` |
| Artifact under test | agent / prompt / skill path |
| Evaluator | name or evaluation model profile |

## Profiles Compared

Reference profiles from `configs/models.yaml`.

| Profile | Provider | Model | Temperature |
|---------|----------|-------|-------------|
| A | TBD | TBD | TBD |
| B | TBD | TBD | TBD |

## Scores

Score each rubric criterion 1-5 per profile.

| Criterion | Profile A | Profile B |
|-----------|-----------|-----------|
| (criterion 1) | | |
| (criterion 2) | | |
| ... | | |
| **Average** | | |
| **Pass?** (per rubric threshold) | | |

## Verdict

- Recommended profile:
- Rationale:
- Tradeoffs (cost, latency, quality):

## Notes & Follow-up

- Notable failures or regressions:
- Run records: `runs/<run-id>.md`, ...
- Update `models/model-matrix.md` if the recommendation changes.
