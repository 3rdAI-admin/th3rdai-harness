# Eval Case: Planner-to-Builder Handoff

## Purpose

Test whether the Planner Agent's output is complete enough for the Builder Agent to begin work without re-asking for context.

## Input

Hand off the plan produced for the `/health` endpoint case (`evals/cases/planning/basic-feature-plan.md`) to the Builder Agent.

## Expected Qualities

- Names the files to create or modify
- Lists implementation steps in execution order
- States explicit, executable validation criteria
- Flags required approvals (dependency installs, commits) up front
- Carries forward open questions and assumptions from planning
- Identifies the next agent and the expected output artifact
- Contains no unresolved ambiguity that blocks a first commit

## Rubric

Use `evals/rubrics/agent-output-quality.md` (emphasis on Handoff readiness and Completeness).
