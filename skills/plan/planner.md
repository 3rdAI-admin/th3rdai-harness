---
description: Create an implementation-ready harness plan from a request
name: plan
---

# Planner - Create Implementation Plan from a Request

Loaded by `/plan` via `skills/plan/SKILL.md` and `configs/agents.yaml` (`planner.default_skill`).

Use the Planner Agent to create a comprehensive implementation-ready plan from an idea, feature, function, fix, refactor, agent change, prompt change, skill change, eval, model profile, config update, framework change, requirement file, PRD, or chat description.

## Harness References

- Agent: `agents/planner.agent.md`
- Prompt: `prompts/planner/v1.md`
- Stage: `stages/01-task-definition/`
- Eval: `evals/rubrics/plan-quality.md`
- Config: `configs/agents.yaml`

## Input: $ARGUMENTS

- Path to `INITIAL.md`, PRD file, issue/spec file, existing plan, or a description of what should be planned

## Process

### 1. Understand the Request

- Read the specified file(s) or use the chat description
- Identify what is being asked for: feature, function, fix, refactor, workflow, integration, agent, prompt, skill, eval, model profile, config, script, documentation, or framework change
- Identify the goal, scope, success criteria, constraints, and assumptions
- Ask clarifying questions if the request is vague or has multiple valid interpretations

### 2. Research and Context

- Read `FRAMEWORK.md`, `CONTEXT.md`, and relevant stage contracts
- Read relevant agent contracts from `agents/`
- Check related prompts, skills, configs, model profiles, evals, and run records
- Explore existing codebase or harness files for patterns
- Identify likely files affected and likely validation requirements

### 3. Create Plan

Write a comprehensive plan to `plans/<plan-name>.md` (see `plans/README.md` for naming and layout). For complex, multi-phase work, use an effort folder `plans/<effort-name>/` with an `EFFORT.md` tracker instead, and add it to `plans/INDEX.md`.

```markdown
# Plan: <Plan Name>

## Goal
<clear one-sentence objective>

## Request Type
<feature|function|fix|refactor|workflow|integration|agent|prompt|skill|eval|model|config|framework|documentation|other>

## Scope
- In scope: <what this plan covers>
- Out of scope: <what this plan intentionally avoids>

## Harness Context
- Agent(s): <relevant agent contracts>
- Skill(s): <relevant skills>
- Prompt(s): <relevant prompt versions>
- Model profile(s): <relevant profiles or TBD>
- Eval(s): <rubrics/cases to use>
- Stage(s): <lifecycle stages involved>

## Assumptions
- <explicit assumptions or none>

## Proposed Approach
<short explanation of the implementation strategy>

## Implementation Steps
1. <step with validation checkpoint>
2. <step with validation checkpoint>
3. ...

## Validation Criteria
- [ ] <specific check>
- [ ] <specific check>

## Safety and Tooling Notes
<approval requirements, destructive-action risks, dependency risks, secret handling>

## Risks and Edge Cases
- <risk or edge case and mitigation>

## Files to Create or Modify
- `path/to/file` - purpose

## Open Questions
- <question or none>

## Recommended Next Agent
<Reviewer|Builder|Evaluator|Researcher>
```

### 4. Output

- Report the plan path created
- Highlight key implementation challenges
- Identify validation and eval requirements
- Suggest next step: `/plan-reviewer` or `/build <plan-path>` after review

## Example Usage

```text
/plan INITIAL.md
/plan "Add a reviewer agent for security-sensitive changes"
/plan "Create an eval case for prompt design quality"
/plan "Refactor the bootstrap scripts to support model profiles"
/plan PRDs/auth-system.md
```

## Success

When complete, suggest review with the Reviewer Agent and implementation with the Builder Agent only after approval.
