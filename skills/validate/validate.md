---
description: Run harness, structure, and artifact validation and report results
name: validate
---

# Validate - Check Harness, Structure, and Artifact Health

Loaded by `/validate` via `skills/validate/SKILL.md`.

Run comprehensive validation for the harness: framework structure, cross-references, implementation changes, and relevant eval/readiness checks. Report what passed, what failed, and what was skipped — honestly.

## Harness References

- Script: `scripts/07-validate-harness.sh`
- Rubrics: `evals/rubrics/`
- Cases: `evals/cases/`
- Runs: `runs/`
- Telemetry: `telemetry/run-log-schema.md`
- Stages: `stages/05-evaluation/`, `stages/07-release/`
- Deployment overlay (optional): `_config/project-notes.md`

## Input: $ARGUMENTS

- Optional scope hint (e.g. "structure only", a changed path, or an artifact to behavior-check)

## Process

### 1. Structural Validation

Run the harness validation script and capture the result:

```bash
scripts/07-validate-harness.sh
```

This checks required files/folders, lifecycle stages, and cross-references (agent contract and `default_skill` paths in `configs/agents.yaml`, routing agents, model profiles, prompt-registry version paths, skill path resolution, and eval case ↔ rubric coherence when that section exists in the validator). A failure here usually means config drift — a renamed or missing file.

Capture the actual summary line (`Passed` / `Warnings` / `Failed`) from the script output — do not assume a fixed check count.

### 2. Change Validation

For implementation changes, run the relevant checks and record each:

- Shell scripts: `bash -n scripts/*.sh`
- Linters/tests for any application code touched
- Re-read changed configs to confirm YAML is well-formed
- If `_config/project-notes.md` exists, run any additional **Verify green** commands listed there (project-specific tests, optional CLIs, etc.)

### 3. Behavior Validation (when applicable)

When a prompt, agent, skill, or model profile changed, validate behavior — do not rely on structure alone:

- Use `evals/rubrics/` and `evals/cases/` via `/eval`
- Record reusable evidence to `evals/results/` and `runs/`
- Use project-specific rubrics/cases named in `_config/project-notes.md` when validating optional subsystems

### 4. Report

```text
VALIDATION REPORT

Structure:  passed | failed (N checks)
Change:     passed | failed | skipped
Behavior:   passed | failed | n/a

Failures:
- <check>: <reason and fix>

Skipped (and why):
- <check>: <reason>

Next:
- Pass -> stages/07-release/ or continue
- Fail -> /revise <artifact> "<finding>"
```

## Safety and Tooling Notes

- Run only approved commands per `configs/tools.yaml`.
- Never report success for checks that were skipped — list them explicitly.
- Do not install dependencies to make a check pass without approval.

## Example Usage

```text
/validate
/validate "structure only"
/validate configs/agents.yaml
/validate prompts/planner/v1.md
/validate src/api/
```

## Success Criteria

- Structural validation result is captured from the script, not assumed.
- Skipped checks are reported honestly with reasons.
- Failures map to a specific fix or `/revise` action.
