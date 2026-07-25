# Skill: skill-script-audit

Invoked by: `/skill-script-audit`

## Procedure

Load and follow `skills/skill-script-audit/skill-script-audit.md` when executing this skill.

## Purpose

Audit existing skills for **steps that should become programmatic scripts**, produce a
migration plan for each candidate, and mine **conversation / session history** for
**new skills worth creating**.

## When to Use

- After a burst of skill authoring when prompts are doing mechanical work that a
  script should own
- Before promoting forged or draft skills into `skills/`
- When the user asks to "script-optimize skills", "find programmatic steps in skills",
  or "what new skills should I create from our chats"
- During Iteration / Release hygiene after major agent workflow changes

## Output

- A **Scriptability Report** listing each audited skill, candidate steps, and a
  concrete migration recipe (script path, CLI, what stays in the skill)
- A **New Skill Backlog** grounded in conversation/session history (with evidence cites)
- Optional: a draft plan path under `plans/` for `/plan-reviewer` → `/build`
  (only if the user asks to implement)

## Safety Contract

- **Read-only by default.** Do not write scripts, rewrite skills, or commit unless the
  user explicitly asks to implement after reviewing the report.
- Never invent history — cite transcript / session / handoff paths for backlog items.
- If implementation is later requested, respect the harness self-modification guard and
  project gates (feature branch / worktree; human merge to shared main).

## Harness References

- Procedure: `skills/skill-script-audit/skill-script-audit.md`
- Related: `skills/revise/`, `skills/research/`, `skills/plan/`
- Deployment overlay (optional): `_config/project-notes.md`
- Stage: `stages/06-iteration/`, `stages/07-release/`

## Next Step

Hand the report to the user. If they approve implementation, run `/plan` on the chosen
migrations / new skills, then `/plan-reviewer`, then `/build`.
