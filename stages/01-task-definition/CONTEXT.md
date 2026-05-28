# Stage 01: Task Definition

## Purpose

Clarify what is being built or changed before any agent, prompt, skill, or config work begins. Define the task, target artifact type, scope, constraints, success criteria, assumptions, and open questions.

## Inputs

| File | Load | Reason |
|------|------|--------|
| User's request | Full | Understand the goal and motivation |
| `FRAMEWORK.md` | Relevant sections | Confirm which harness layer the work belongs to |
| `CONTEXT.md` | Routing table | Confirm this is the right stage and what comes next |
| Relevant `agents/*.agent.md` | Targeted | Identify the responsible agent, if known |
| Relevant `evals/rubrics/` | Targeted | Note how success will eventually be measured |

## Process

1. Restate the request in your own words and identify the target artifact (agent, skill, prompt, model profile, eval, config, script, or docs).
2. Identify 3-5 clarifying questions that materially change the approach.
3. Define explicit success criteria and acceptance checks.
4. Capture scope boundaries — what is in scope and what is explicitly out of scope.
5. Record constraints, assumptions, and dependencies.
6. List open questions and who must answer them.
7. Recommend the next stage and responsible agent.

## Outputs

| File | Location | Format |
|------|----------|--------|
| Task definition | `output/task-definition.md` | Markdown with scope, success criteria, constraints |
| Open questions | `output/open-questions.md` | Numbered list with owners |

## Checkpoint

**Stop here and ask the user to confirm** the task definition, success criteria, and scope before proceeding to Stage 02 (Agent Design) or the appropriate next stage.
