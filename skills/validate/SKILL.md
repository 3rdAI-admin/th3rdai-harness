# Skill: validate

Invoked by: /validate command

## Procedure

Load and follow `skills/validate/validate.md` when executing this skill.

## Purpose
Run comprehensive validation for the harness, project structure, implementation changes, and relevant eval/readiness checks.

## When to Use
- After `/build` to verify
- Anytime to check project health
- Before `stages/07-release/`
- After changing agents, prompts, configs, evals, stages, scripts, or application code

## Output
Validation report with pass/fail status, skipped checks, command results, structural findings, and recommended fixes.

## Harness Checks
- Run `scripts/07-validate-harness.sh` for framework structure validation
- Run project-specific checks from `_config/project-notes.md` when present
- Use `evals/rubrics/` and `evals/cases/` when validating agent, prompt, skill, or model behavior
- Record notable runs in `runs/` when validation produces reusable evidence

## Harness References
- Procedure: `skills/validate/validate.md`
- Script: `scripts/07-validate-harness.sh`
- Stage: `stages/05-evaluation/`
- Stage: `stages/07-release/`
- Telemetry: `telemetry/run-log-schema.md`
- Deployment overlay (optional): `_config/project-notes.md`
