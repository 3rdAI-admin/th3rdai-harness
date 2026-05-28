# Eval Case: Failing Test Diagnosis

## Purpose

Test whether an agent can diagnose a failing test from its output, identify the root cause, and propose a minimal fix scoped to the actual defect.

## Input

A test suite reports one failure: `test_parse_date` expects `2026-05-28` but receives `2026-28-05`. Given the failing test, the function under test, and the stack trace, diagnose and propose a fix.

## Expected Qualities

- Identifies the root cause (month/day order swapped in the format string)
- Distinguishes the defect from incidental test noise
- Proposes the smallest fix that addresses the root cause
- Does not refactor or expand scope beyond the bug
- States how to confirm the fix (re-run the failing test plus related cases)
- Notes any regression risk to other date-format callers

## Rubric

Use `evals/rubrics/agent-output-quality.md` for the diagnosis; use `evals/rubrics/plan-quality.md` if a multi-step fix plan is produced.
