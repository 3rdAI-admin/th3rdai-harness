# AI Agent Development Harness Revision Notes

## Summary

The repository has been revised from a three-stage ICM content/workflow template into an AI agent/model development harness.

The harness now emphasizes:

- Explicit agent contracts
- Reusable skills
- Versioned prompts
- Model profiles
- Evaluation rubrics and cases
- Tool safety policies
- Run records
- Lifecycle stages from task definition through release

## Major Structural Changes

### Added Framework Layers

- `FRAMEWORK.md`
- `agents/`
- `prompts/`
- `models/`
- `configs/`
- `evals/`
- `runs/`
- `telemetry/`

### Revised Lifecycle Stages

The old content-oriented stages:

```text
research → draft → review
```

were replaced with:

```text
task-definition → agent-design → prompt-design → tool-integration → evaluation → iteration → release
```

### Added Default Agents

- `researcher.agent.md`
- `planner.agent.md`
- `builder.agent.md`
- `reviewer.agent.md`
- `evaluator.agent.md`

### Added Initial Evaluation Assets

- Plan quality rubric
- Tool safety rubric
- Agent output quality rubric
- Basic feature planning eval case

### Added Machine-Readable Configs

- `configs/agents.yaml`
- `configs/models.yaml`
- `configs/routing.yaml`
- `configs/tools.yaml`

## Current Validation

Use:

```bash
scripts/07-validate-harness.sh
```

The checked-in harness currently validates the expected framework structure, routing, agents, configs, stages, prompts, evals, and telemetry files.

## Remaining Improvement Area

The older tutorial scripts still reflect parts of the original ICM onboarding flow. The checked-in harness structure is aligned, but future work should update the full bootstrap flow so new projects are generated with the agent harness layout by default.
