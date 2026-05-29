# Skill: debug

Invoked by: /debug command

## Procedure

Load and follow `skills/debug/debug.md` when executing this skill.

## Purpose
Systematically diagnose a failure — a failing test, error, or unexpected behavior — identify the root cause from evidence, and propose the smallest fix scoped to the actual defect.

## When to Use
- A test, build, validation, or eval fails and the cause is not obvious
- Behavior differs from what a plan, prompt, or contract specifies
- During `stages/06-iteration/` when a regression must be understood before revising

## Output
A diagnosis tied to evidence (logs, stack traces, file lines), a stated root cause, a minimal proposed fix, a confirmation method, and noted regression risk.

## Harness References
- Procedure: `skills/debug/debug.md`
- Agents: `agents/researcher.agent.md` (investigation), `agents/builder.agent.md` (fix)
- Rubrics: `evals/rubrics/agent-output-quality.md`
- Case: `evals/cases/debugging/failing-test-diagnosis.md`
- Stage: `stages/06-iteration/`
- Deployment overlay (optional): `_config/project-notes.md`

## Next Step
- Root cause found: hand the minimal fix to the Builder Agent via `/build`, or `/revise` the source artifact if the defect is in a plan/prompt/config.
- Cause still unclear: record findings and escalate with specific open questions.
