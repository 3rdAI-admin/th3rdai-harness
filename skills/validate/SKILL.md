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

## Autonomy Audit Verification

When validating orchestrator execution (v1.2.0+):

1. **Check audit log exists:** `runs/autonomy-decisions.jsonl`
2. **Verify decision alignment:**
   - Count auto-approved vs user-approved vs blocked decisions
   - Confirm risk classifications match operation types
   - Check CRITICAL operations were handled appropriately
3. **Sample validation:**
   ```bash
   # View last 10 decisions
   tail -10 runs/autonomy-decisions.jsonl | python3 -c "import sys, json; [print(json.dumps(json.loads(l), indent=2)) for l in sys.stdin]"
   ```
4. **Report findings:** Include autonomy summary in validation output

## Harness References
- Procedure: `skills/validate/validate.md`
- Script: `scripts/07-validate-harness.sh`
- Stage: `stages/05-evaluation/`
- Stage: `stages/07-release/`
- Telemetry: `telemetry/run-log-schema.md`
- Deployment overlay (optional): `_config/project-notes.md`
