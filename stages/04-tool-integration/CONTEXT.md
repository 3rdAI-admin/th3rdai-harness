# Stage 04: Tool Integration

## Purpose

Define, review, or implement tool permissions, runtime behavior, scripts, and integrations used by agents or skills.

## Inputs

| File | Load | Reason |
|------|------|--------|
| `FRAMEWORK.md` | Relevant sections | Follow harness principles |
| `configs/tools.yaml` | Full | Apply tool safety policies |
| Relevant `agents/*.agent.md` | Targeted | Align permissions with agent contracts |
| Relevant `skills/` files | Targeted | Understand tool usage expectations |
| Relevant scripts | Targeted | Understand runtime behavior |

## Process

1. Identify the tool, command, script, or integration being added or changed.
2. Classify the action as read-only, write-limited, command-safe, or high-risk.
3. Define allowed and disallowed actions.
4. Add approval checkpoints for dependency installation, destructive commands, long-running servers, and git mutation.
5. Update scripts, skill instructions, or `configs/tools.yaml` as needed.
6. Document validation steps.

## Outputs

| File | Location | Format |
|------|----------|--------|
| Tool policy updates | `configs/tools.yaml` | YAML |
| Script updates | `scripts/` | Shell or project language |
| Integration notes | `output/tool-integration-notes.md` | Markdown |

## Checkpoint

Stop for human approval before enabling tools that can mutate external state, install dependencies, delete files, access secrets, or commit changes.
