# Plan: CLI + Eval Hook

## Goal

Expose the orchestrator as a simple CLI and let it invoke eval cases against rubrics, recording results.

## Request Type

feature (harness tooling)

## Scope

- In scope: an `argparse` CLI (`scripts/orchestrate.py`) wrapping the sequencer; an eval mode that pairs an `evals/cases/` case with its `evals/rubrics/` rubric and writes an `evals/results/` record.
- Out of scope: automated scoring by a model (the eval hook prepares the case + rubric bundle and records the human/agent verdict), networked execution, dependencies.

## Harness Context

- Agent(s): Builder, Reviewer, Evaluator
- Depends on: `plans/native-orchestrator/02-sequencer.md`
- Skill(s): `skills/eval/eval.md`, `skills/validate/validate.md`
- Evals: `evals/cases/`, `evals/rubrics/`, `evals/results/`

## Proposed Approach

`scripts/orchestrate.py` with subcommands:

- `route <name>` — run the sequencer for a lifecycle route. Always dry-run in this phase; the opt-in `--execute` mode is introduced in Phase 04.
- `eval <case-path> [--rubric <path>]` — resolve the rubric (explicit `--rubric`, else the case's own `## Rubric` section — e.g. `evals/cases/planning/basic-feature-plan.md` names `plan-quality.md`), assemble the case + rubric bundle, then write an `evals/results/<run-id>.md` stub plus a run record for the Evaluator to complete.
- `--help` documents all subcommands.

## Implementation Steps

1. Build the `argparse` CLI delegating to `sequencer`/`runlog`. (validation: `python3 scripts/orchestrate.py --help` lists subcommands)
2. Implement `eval` subcommand: resolve the rubric (`--rubric`, else the case's `## Rubric` section), bundle case + rubric, and write result + run stubs. (validation: running against `evals/cases/planning/basic-feature-plan.md` *without* `--rubric` resolves `plan-quality.md` from the case and produces an `evals/results/` file)
3. Document usage in `skills/eval/eval.md` and `README.md`. (validation: skill-reference check in validator still passes)

## Validation Criteria

- [ ] `python3 scripts/orchestrate.py --help` works with no dependencies
- [ ] `eval` produces an `evals/results/` record paired to the correct rubric (resolved from `--rubric` or the case's `## Rubric` section)
- [ ] `route <name>` produces dry-run run records for a full lifecycle route
- [ ] `scripts/07-validate-harness.sh` still passes

## Safety and Tooling Notes

- Stdlib only; no installs.
- Eval hook prepares context and records verdicts — it does not fabricate scores.

## Risks and Edge Cases

- Rubric resolution order: explicit `--rubric`, else parse the case's `## Rubric` section; if neither yields a path, fail with guidance.
- Result filename collisions → use timestamped run-ids.

## Files to Create or Modify

- `scripts/orchestrate.py` - CLI entry point
- `skills/eval/eval.md` - document the CLI eval hook
- `README.md` - note the optional orchestrator usage

## Recommended Next Agent

Reviewer
