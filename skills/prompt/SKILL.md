# Skill: prompt

Invoked by: /prompt command

## Purpose
Create a focused one-off prompt or draft a reusable prompt version for an agent, skill, eval, or harness workflow.

## When to Use
- Single focused prompt task
- Prompt output-format refinement
- Agent instruction draft
- Small prompt safety or verification improvement
- During `stages/03-prompt-design/`

## Output
Structured prompt saved to `prompts/one-off/` or a versioned prompt saved to `prompts/<name>/vN.md`, with registry/changelog updates when reusable.

## Harness References
- Procedure: `skills/prompt/prompt.md`
- Stage: `stages/03-prompt-design/`
- Registry: `prompts/registry.md`
- Eval: `evals/rubrics/agent-output-quality.md`
- Deployment overlay (optional): `_config/project-notes.md`

## Note
For broad features, agent redesigns, or multi-step framework changes, use `/plan` first.
