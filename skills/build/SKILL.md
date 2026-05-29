# Skill: build

Invoked by: /build command

## Purpose
Use the Builder Agent to implement an approved plan or PRP, validate the result, and summarize changes.

## When to Use
- After `/plan` creates a reviewed plan or PRP
- During `stages/04-tool-integration/`, `stages/06-iteration/`, or approved implementation work
- When changes to agents, skills, prompts, evals, configs, scripts, docs, or application code are ready to make

## Output
Implements approved changes, runs relevant validation, records skipped checks honestly, and summarizes files changed, validation results, risks, and next steps.

## Harness References
- Procedure: `skills/build/build.md`
- Agent: `agents/builder.agent.md`
- Config: `configs/tools.yaml`
- Validation: `skills/validate/validate.md`
- Release stage: `stages/07-release/`
- Deployment overlay (optional): `_config/project-notes.md`

## Next Step
- Success: run `/validate` or move to `stages/05-evaluation/` or `stages/07-release/`
- Failure: run `/revise` or return to the Planner Agent with findings
