# Telemetry

Telemetry captures what happened during agent, skill, prompt, model, and evaluation runs.

The goal is observability, not surveillance. Do not record secrets or sensitive user data unless explicitly required and approved.

## Recommended Run Record Fields

- Run ID
- Date/time
- User request summary
- Agent
- Skill
- Prompt version
- Model profile
- Input files
- Output files
- Tool actions
- Validation results
- Eval scores
- Issues found
- Follow-up actions

## Storage

Store human-readable run records in `runs/` unless a project adopts a structured database or external tracking system.
