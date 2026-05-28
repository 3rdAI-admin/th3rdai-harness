# Run Log Schema

Use this schema for markdown or YAML run records.

```yaml
run_id: YYYYMMDD-HHMMSS-short-name
created_at: ISO-8601 timestamp
request: short summary
agent: planner|builder|reviewer|researcher|evaluator
skill: optional skill path
prompt_version: optional prompt path
model_profile: optional profile name
inputs:
  - path or description
outputs:
  - path or description
tool_actions:
  - description
validation:
  status: passed|failed|skipped
  notes: summary
evaluation:
  rubric: optional path
  score: optional number
  notes: summary
issues:
  - severity: high|medium|low
    description: issue summary
follow_up:
  - next action
```
