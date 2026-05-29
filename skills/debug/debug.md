---
description: Diagnose a failure from evidence and propose a minimal fix
name: debug
---

# Debug - Diagnose a Failure and Propose a Minimal Fix

Loaded by `/debug` via `skills/debug/SKILL.md`.

Investigate a failure using evidence, not guesses. The goal is a root cause supported by file:line evidence and the smallest fix that addresses it — never a speculative rewrite.

## Harness References

- Agents: `agents/researcher.agent.md`, `agents/builder.agent.md`
- Rubric: `evals/rubrics/agent-output-quality.md`
- Case: `evals/cases/debugging/failing-test-diagnosis.md`
- Stage: `stages/06-iteration/`
- Telemetry: `telemetry/run-log-schema.md`
- Deployment overlay (optional): `_config/project-notes.md`

## Input: $ARGUMENTS

- A failure description, error message, failing test, or unexpected behavior
- Optional: the relevant output (logs, stack trace) and the artifact under suspicion

## Process

### 1. Reproduce and Capture Evidence

- Identify the exact failing command, test, or behavior.
- Capture the real output (error text, stack trace, diff between expected and actual).
- Do not theorize before you have observed the failure.
- If `_config/project-notes.md` exists, check its **Debug shortcuts** table for project-specific repro commands.

**Common harness repro commands (when present in the project):**

| Area | Command |
|------|---------|
| Harness structure | `scripts/07-validate-harness.sh` |
| Shell scripts | `bash -n scripts/*.sh` |
| Project tests | per `_config/project-notes.md` or the project's README |

### 2. Localize

- Trace the evidence to specific files and lines.
- Read the actual code/artifact at those locations — confirm shape and conventions, do not assume.
- Narrow from symptom to the smallest region that could produce it.

### 3. Form and Test a Hypothesis

```markdown
## Hypothesis
- Suspected cause: <statement>
- Evidence for: <file:line, log line>
- Evidence against / ruled out: <what you checked>
```

Prefer the simplest cause consistent with all evidence. Distinguish the defect from incidental noise.

### 4. State Root Cause and Minimal Fix

```markdown
## Root Cause
<one clear statement, cited to file:line>

## Minimal Fix
- <smallest change that addresses the root cause>

## Confirmation
- <how to verify: re-run the failing check plus related cases>

## Regression Risk
- <other callers/paths that could be affected>
```

### 5. Output

```text
DEBUG COMPLETE: <failure>

Root cause: <statement> (<file:line>)
Minimal fix: <summary>
Confirm by: <command/check>
Regression risk: <scope>

Next:
- /build  (apply the fix within scope)
- /revise <artifact>  (if the defect is in a plan/prompt/config)
```

## Safety and Tooling Notes

- Investigation is read-only; do not change code while diagnosing.
- Run only approved commands per `configs/tools.yaml`; reproducing a failure must not run destructive commands without approval.
- Keep the fix scoped to the defect — no opportunistic refactors.

## Example Usage

```text
/debug "test_parse_date expects 2026-05-28 but gets 2026-28-05"
/debug "scripts/07-validate-harness.sh exits 1 after the rename"
/debug "planner skill loads the wrong file"
/debug "<application test> fails with unexpected status code"
```

## Success Criteria

- Root cause is supported by cited evidence, not speculation.
- The proposed fix is minimal and scoped to the defect.
- A concrete confirmation method and regression risk are stated.
