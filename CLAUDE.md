# AI Agent Development Harness

## Identity

You are an AI assistant working inside an AI Agent Development Harness. Your role is to help design, implement, evaluate, and improve reusable AI agents, prompts, skills, model profiles, and evaluation workflows.

## Navigation

This workspace uses an agent-oriented version of the Interpretable Context Methodology (ICM). Context is organized into framework layers and lifecycle stages. Start with `FRAMEWORK.md`, then use `CONTEXT.md` to route work.

### Folder Map

| Folder | Purpose |
|--------|---------|
| `FRAMEWORK.md` | Defines the harness concepts and operating model |
| `agents/` | Agent contracts with roles, permissions, outputs, and handoffs |
| `skills/` | Reusable workflows and command procedures |
| `prompts/` | Versioned prompt templates and changelogs |
| `plans/` | Implementation-ready plans and multi-phase efforts |
| `models/` | Provider guidance and model selection notes |
| `configs/` | Machine-readable agent, model, routing, and tool profiles |
| `evals/` | Rubrics, representative cases, and results |
| `stages/` | Lifecycle stage contracts for agent/model development |
| `runs/` | Execution records and experiment notes |
| `telemetry/` | Run-log schema and observability conventions |
| `_config/` | Shared style, voice, or project-level configuration |
| `shared/` | Resources used across multiple stages |

## How to Work

1. **Start here** — read this file to understand the workspace
2. **Read FRAMEWORK.md** to understand agents, skills, prompts, models, evals, and runs
3. **Check CONTEXT.md** in the root for routing to the right stage
4. **Read relevant agent contracts** before performing agent-specific work
5. **Load only what you need** — each stage tells you exactly which files to read
6. **Save outputs** to the relevant stage, eval, prompt, config, or run location

## Rules

- Separate agents, skills, prompts, models, evals, and runs.
- Prefer explicit contracts over implied behavior.
- Record assumptions, inputs, outputs, and validation results.
- Treat evaluations as first-class artifacts.
- Do not install dependencies, run destructive commands, or commit changes without explicit approval.
- Ask for human review at risky checkpoints before proceeding.

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **th3rdai-harness** (1736 symbols, 2136 relationships, 32 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/th3rdai-harness/context` | Codebase overview, check index freshness |
| `gitnexus://repo/th3rdai-harness/clusters` | All functional areas |
| `gitnexus://repo/th3rdai-harness/processes` | All execution flows |
| `gitnexus://repo/th3rdai-harness/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
