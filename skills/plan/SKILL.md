# Skill: plan

Invoked by: /plan command

## Purpose
Use the Planner Agent to create an implementation-ready plan for a feature, agent, prompt, skill, eval, model profile, config, or framework change.

## When to Use
- During `stages/01-task-definition/` or before `stages/02-agent-design/`, `stages/03-prompt-design/`, or implementation work
- When a request needs scope, assumptions, risks, affected files, and validation criteria
- Before invoking the Builder Agent

## Output
Creates a plan or PRP with goal, scope, context, implementation steps, validation criteria, risks, affected files, open questions, and recommended next agent.

## Harness References
- Agent: `agents/planner.agent.md`
- Prompt: `prompts/planner/v1.md`
- Config: `configs/agents.yaml`
- Eval: `evals/rubrics/plan-quality.md`

## Next Step
Run `/plan-reviewer` or use `agents/reviewer.agent.md` for review, then run `/build <plan-path>` when approved.

## Related Skill: plan-reviewer

Invoked by: /plan-reviewer command

### Purpose
Use the Reviewer Agent to review and improve an existing plan or PRP before implementation.

### When to Use
- When you have a new plan that has just been created
- When asked by a human to review a plan
- When called by another agent or skill
- Before starting implementation
- Before releasing a major harness change

### Output
Updates the relevant plan or PRP with fixes, implementation guidance, testing coverage, safety notes, and evaluation gaps.

### Next Step
Run `/build <plan-path>` after review findings are resolved.