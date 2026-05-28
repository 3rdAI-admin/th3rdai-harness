# Prompt Registry

Use this registry to track reusable prompt templates, their versions, target agents, compatible models, and evaluation status.

| Prompt | Current Version | Agent | Purpose | Eval Status |
|--------|-----------------|-------|---------|-------------|
| Planner Prompt | `planner/v1.md` | Planner | Create implementation-ready plans | Not evaluated |
| Reviewer Prompt | `reviewer/v1.md` | Reviewer | Review plans and implementations | Not evaluated |

## Versioning Rules

- Create a new version when behavior changes materially.
- Record why the prompt changed.
- Link prompt versions to eval results when available.
- Do not overwrite historical versions just to hide failed behavior.
