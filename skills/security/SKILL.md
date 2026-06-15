# Skill: security

Invoked by: `/security` command

## Procedure

Load and follow `skills/security/security.md` when executing this skill.

## Purpose

Review code diffs or deployment posture for security defects in any web application.
Evidence-based, read-only review with cited `file:line` findings and a clear verdict.

## When to Use

- Before merging changes that touch auth, sessions, uploads, APIs, or security headers
- Before exposing a dev server on a LAN or behind a reverse proxy
- After a security-related bug report or incident
- During `stages/07-release/` as a gate alongside `/validate`
- When `/plan-reviewer` flags safety gaps and a deeper security pass is needed

## Modes

| Mode | Input | Output |
|------|-------|--------|
| `diff` (default) | Git diff, PR, or file list | Findings with severity, impact, fix, verdict |
| `threat-model` | Deployment scenario (localhost / LAN / internet) | Required controls, gaps, go/no-go |

Pass the mode as the first token in `$ARGUMENTS` when not doing a default diff review.

For project-specific **baseline regression audits** (e.g. a shipped WASA report), use a
deployment overlay skill such as `skills/security-<project>/` or `_config/security-baseline.md`
with a companion procedure — not this portable skill.

## Output

A security review report with:

- Stated threat model (localhost vs LAN vs internet)
- Findings table: ID, severity, location (`file:line`), impact, fix
- Blocking vs advisory classification
- Verdict: **block**, **approve-with-changes**, or **approve**
- Handoff: `/build` for fixes, `/revise` for plan gaps, or release sign-off

## Harness References

- Procedure: `skills/security/security.md`
- Agent: `agents/reviewer.agent.md` (read-only review posture)
- Rubrics: `evals/rubrics/agent-output-quality.md`, `evals/rubrics/tool-safety.md`
- Eval case: `evals/cases/code-review/security-bug-review.md`
- Optional baseline overlay: `_config/security-baseline.md` (per-project; see template)
- Deployment overlay (optional): `_config/project-notes.md`
- Stage: `stages/07-release/`

## Next Step

- **block** or **approve-with-changes:** hand findings to `/build` with priority ordering, or `/revise` the plan.
- **approve:** proceed to `/validate` and release workflow.
