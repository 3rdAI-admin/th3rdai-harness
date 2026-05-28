# Eval Case: Prompt Revision

## Purpose

Test whether a Stage 03 (Prompt Design) revision improves a measured weakness without regressing existing behavior, and whether it is versioned and documented correctly.

## Input

The current `prompts/planner/v1.md` produces plans that consistently omit risk and edge-case analysis. Revise the prompt so plans include a dedicated risk section, and ship it as a new version.

## Expected Qualities

- New version saved as `prompts/planner/v2.md` (v1 left untouched)
- `prompts/planner/changelog.md` records what changed and why
- `prompts/registry.md` updated to point at the new version
- The change is the smallest edit that addresses the weakness
- States which eval case and rubric will confirm the improvement
- No regression to goal clarity, scope, or handoff sections

## Rubric

Use `evals/rubrics/agent-output-quality.md`.
