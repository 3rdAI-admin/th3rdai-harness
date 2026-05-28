# Eval Case: Security Bug Review

## Purpose

Test whether the Reviewer Agent surfaces a real security defect in a diff, explains the impact, and proposes a concrete fix without raising noisy false positives.

## Input

Review a diff that adds a search endpoint building a SQL query via string concatenation of a user-supplied `q` parameter, and that logs the full request (including an `Authorization` header) at info level.

## Expected Qualities

- Identifies the SQL injection and names the vulnerable line
- Identifies the secret/token leak in logs
- Explains impact and severity for each finding
- Proposes concrete fixes (parameterized query; redact sensitive headers)
- Distinguishes blocking issues from nits
- Does not invent issues unsupported by the diff
- Clear verdict and handoff (block vs. approve-with-changes)

## Rubric

Use `evals/rubrics/agent-output-quality.md`.
