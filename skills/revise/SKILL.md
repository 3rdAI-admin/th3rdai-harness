# Skill: revise

Invoked by: /revise command

## Procedure

Load and follow `skills/revise/revise.md` when executing this skill.

## Purpose
Revise a plan, prompt, skill, agent, model profile, config, or eval when validation or evaluation reveals design-level issues.

## When to Use
- `/build`, `/validate`, review, or `/eval` surfaces a flaw in the source artifact or plan
- During `stages/06-iteration/`
- Wrong approach, missing steps, unsafe tool policy, or weak eval coverage

## Output
Updated artifact with revised approach, validation criteria, and iteration evidence when useful.

## Harness References
- Procedure: `skills/revise/revise.md`
- Stage: `stages/06-iteration/`
- Agents: `agents/planner.agent.md`, `agents/reviewer.agent.md`, `agents/evaluator.agent.md`
- Deployment overlay (optional): `_config/project-notes.md`

## Next Step
Re-run `/build`, `/validate`, or `/eval` with the revised artifact.