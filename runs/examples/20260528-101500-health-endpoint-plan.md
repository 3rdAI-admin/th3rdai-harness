# Run: Health Endpoint Plan

Example run record (Planner Agent producing a plan). Conforms to `telemetry/run-log-schema.md`.

```yaml
run_id: 20260528-101500-health-endpoint-plan
created_at: 2026-05-28T10:15:00Z
request: Produce an implementation-ready plan for a new /health endpoint
agent: planner
skill: skills/plan/SKILL.md
prompt_version: prompts/planner/v1.md
model_profile: planning
inputs:
  - evals/cases/planning/basic-feature-plan.md
outputs:
  - stages/01-task-definition/output/task-definition.md
  - plan with goal, files, steps, validation, risks, handoff
tool_actions:
  - read-only inspection of existing API routes
validation:
  status: passed
  notes: Plan includes concrete validation steps and a Builder handoff.
evaluation:
  rubric: evals/rubrics/plan-quality.md
  score: 4.2
  notes: See runs/examples/20260528-103000-health-plan-eval.md
issues:
  - severity: low
    description: Uptime source (process vs. system) left as an open question.
follow_up:
  - Hand off to Builder Agent (Stage 04 / build skill)
```
