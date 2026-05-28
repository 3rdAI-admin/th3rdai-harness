# Agent Harness Routing

This file tells you where to go based on what kind of agent/model harness work the user needs.

## Stage Routing

| If the user wants to... | Go to... |
|------------------------|----------|
| Clarify a task, requirement, workflow, or success criteria | `stages/01-task-definition/` |
| Define or revise an agent role, permissions, outputs, or handoff | `stages/02-agent-design/` |
| Create or revise prompts, prompt versions, or prompt changelogs | `stages/03-prompt-design/` |
| Define tool permissions, runtime behavior, scripts, or integrations | `stages/04-tool-integration/` |
| Create or run rubrics, test cases, model comparisons, or eval reports | `stages/05-evaluation/` |
| Improve an agent, prompt, skill, model profile, or workflow from findings | `stages/06-iteration/` |
| Prepare a stable version for use, documentation, or commit | `stages/07-release/` |

## How Routing Works

1. Read the user's request
2. Match it to the correct stage using the table above
3. Navigate to that stage's folder
4. Read the stage's `CONTEXT.md` for detailed instructions
5. Read relevant files from `agents/`, `skills/`, `prompts/`, `models/`, `configs/`, or `evals/`

## Shared Resources

If a stage's CONTEXT.md references shared files, find them in:

- `FRAMEWORK.md` — Harness concepts and operating principles
- `agents/` — Role contracts and handoff rules
- `prompts/` — Versioned prompt templates
- `models/` — Provider/model guidance
- `configs/` — Agent, model, routing, and tool policies
- `evals/` — Rubrics, cases, and results
- `_config/` — Brand voice, style guides, design tokens
- `shared/` — Templates, examples, and cross-stage resources
- `skills/` — Reusable domain knowledge and workflows
