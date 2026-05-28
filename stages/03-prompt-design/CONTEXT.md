# Stage 03: Prompt Design

## Purpose

Create or revise the versioned prompt template used by an agent or skill, and keep its changelog and registry entry current. Prompts answer the question **what exact instruction pattern is being tested or reused?**

## Inputs

| File | Load | Reason |
|------|------|--------|
| `../01-task-definition/output/task-definition.md` | Full | Anchor the prompt to the confirmed task |
| Relevant `agents/<name>.agent.md` | Full | Align the prompt with the agent's role and outputs |
| `prompts/registry.md` | Full | Keep the prompt registry consistent |
| Existing `prompts/<name>/` | Full if present | Preserve version history and changelog format |
| Relevant `evals/rubrics/` | Targeted | Design the prompt against how it will be scored |

## Process

1. Identify the agent or skill the prompt serves and the behavior it must produce.
2. Decide whether to create a new prompt track or a new version of an existing one.
3. Draft the prompt with explicit instructions, inputs, and output format.
4. Save it as `prompts/<name>/vN.md` (or `prompts/one-off/` for single-use prompts).
5. Update `prompts/<name>/changelog.md` with what changed and why.
6. Update `prompts/registry.md` so the new version is discoverable.
7. Note which eval case and rubric will validate the prompt.

## Outputs

| File | Location | Format |
|------|----------|--------|
| Prompt version | `prompts/<name>/vN.md` | Markdown template |
| Changelog entry | `prompts/<name>/changelog.md` | Markdown |
| Registry update | `prompts/registry.md` | Markdown |
| Design notes | `output/prompt-design-notes.md` | Markdown |

## Checkpoint

**Stop here and ask the user to review** the new prompt version before proceeding to Stage 04 (Tool Integration) or Stage 05 (Evaluation). Do not overwrite an existing prompt version — always create a new `vN`.
