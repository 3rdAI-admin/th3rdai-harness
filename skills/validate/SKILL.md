# Skill: validate

Invoked by: /validate command

## Purpose
Run comprehensive validation for the harness, project structure, implementation changes, and relevant eval/readiness checks.

## When to Use
- After `/build` to verify
- Anytime to check project health
- Before `stages/07-release/`
- After changing agents, prompts, configs, evals, stages, or scripts

## Output
Validation report with pass/fail status, skipped checks, command results, structural findings, and recommended fixes.

## Harness Checks
- Run `scripts/07-validate-harness.sh` for framework structure validation
- Use `evals/rubrics/` when validating agent, prompt, skill, or model behavior
- Record notable runs in `runs/` when validation produces reusable evidence

## Harness References
- Stage: `stages/05-evaluation/`
- Stage: `stages/07-release/`
- Telemetry: `telemetry/run-log-schema.md`
