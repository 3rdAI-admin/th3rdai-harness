# Skill: run

Invoked by: /run command

## Purpose
Start an application, demo, harness workflow, or approved runtime target in development mode.

## When to Use
- After successful `/build`
- To test the application or workflow
- During `stages/04-tool-integration/` to verify runtime behavior
- During `stages/05-evaluation/` when evals require a running target

## Output
Starts the approved runtime target, reports the command, URL or process details, and next validation steps.

## Harness References
- Agent: `agents/builder.agent.md`
- Tool policy: `configs/tools.yaml`
- Runs: `runs/`
