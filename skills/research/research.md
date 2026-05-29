---
description: Gather grounded context before planning or implementation
name: research
---

# Research - Gather Grounded Context Before Planning

Loaded by `/research` via `skills/research/SKILL.md` and `configs/agents.yaml` (`researcher.default_skill`).

Use the Researcher Agent to collect the context needed to plan or implement safely. The goal is grounded findings tied to sources, not guesses.

## Harness References

- Agent: `agents/researcher.agent.md`
- Stage: `stages/01-task-definition/`
- Framework: `FRAMEWORK.md`
- Evals: `evals/README.md`, `evals/cases/`, `evals/rubrics/`
- Deployment overlay (optional): `_config/project-notes.md`

## Input: $ARGUMENTS

- A request, question, or task description
- Optional: paths or references the user wants prioritized

## Process

### 1. Frame the Question

- Restate what must be understood before work can proceed.
- List the specific unknowns that would change the approach.

### 2. Gather From Primary Sources

- Read relevant project files, configs, agent contracts, and stage contracts.
- Search the workspace for the symbols, conventions, and patterns the task touches.
- If `_config/project-notes.md` exists, read it for deployment-specific resume paths and tooling — do not assume every project has the same optional components.
- Read approved external references only when needed and permitted by `configs/tools.yaml`.
- Tie every finding to a file path or source — if you cannot cite it, mark it as an assumption.

### 3. Separate Facts From Assumptions

```markdown
## Findings
- fact: <statement> (source: <path or reference>)
- assumption: <statement> (needs confirmation)

## Constraints
- <constraint and where it comes from>

## Open Questions
- <question and who must answer it>
```

### 4. Output

```text
RESEARCH COMPLETE: <topic>

Key findings:
- <fact with source>

Assumptions to confirm:
- <assumption>

Open questions:
- <question>

Recommended next step:
- /plan <request>  (hand findings to the Planner Agent)
```

## Safety and Tooling Notes

- Read-only: do not modify source files, install dependencies, or commit changes.
- Do not read secret files unless explicitly required and approved per `configs/tools.yaml`.
- Stop and ask when requirements are ambiguous rather than guessing.

## Example Usage

```text
/research "how does the harness validation script decide pass/fail?"
/research "what conventions do existing skills follow before I add a new one?"
/research configs/tools.yaml "what tool tiers exist and what needs approval?"
/research "what application code owns authentication in this repo?"
```

## Success Criteria

- The task context is clear and grounded in cited sources.
- Facts are separated from assumptions.
- Open questions and constraints are explicit.
- The Planner Agent has enough context to proceed.
