# Agents

Agents are role-based actors with explicit responsibilities, permissions, outputs, and handoff rules.

Use this folder to define reusable AI agents that can operate across projects, skills, prompts, models, and evaluations.

## Agent Contract Template

Each `*.agent.md` file should include:

- Purpose
- Inputs
- Outputs
- Tools allowed
- Tools disallowed
- Operating rules
- Success criteria
- Failure modes
- Handoff rules

## Default Agents

| Agent | Purpose |
|-------|---------|
| `researcher.agent.md` | Gather context, sources, and constraints |
| `planner.agent.md` | Create implementation-ready plans |
| `builder.agent.md` | Implement approved plans safely |
| `reviewer.agent.md` | Review quality, risks, and completeness |
| `evaluator.agent.md` | Run rubrics, test cases, and model comparisons |
