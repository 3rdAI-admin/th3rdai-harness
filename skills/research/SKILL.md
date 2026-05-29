# Skill: research

Invoked by: /research command

## Procedure

Load and follow `skills/research/research.md` when executing this skill.

## Purpose
Use the Researcher Agent to gather context, source material, constraints, examples, and assumptions before planning or implementation.

## When to Use
- At the start of `stages/01-task-definition/`, before `/plan`
- When a request references unfamiliar code, conventions, or external material
- When assumptions must be grounded in actual files before committing to an approach

## Output
Produces a research summary with a source list (file paths or references), assumptions, constraints, and open questions, ready to hand to the Planner Agent.

## Harness References
- Procedure: `skills/research/research.md`
- Agent: `agents/researcher.agent.md`
- Stage: `stages/01-task-definition/`
- Config: `configs/agents.yaml`

## Next Step
Hand findings to the Planner Agent via `/plan`, or to the Evaluator Agent when the research supports an evaluation.
