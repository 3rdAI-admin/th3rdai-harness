# Skill: e2e-test

Invoked by: /tests/e2e-test.md command

## Purpose
Run comprehensive testing for implemented applications or harness workflows, including end-to-end browser testing when a UI exists.

## When to Use
- After successful `/build`
- Before code review or release
- When validating user journeys, UI behavior, and data persistence
- During `stages/05-evaluation/` when a workflow needs evidence beyond static review

## Output
Tests user journeys or representative harness cases, captures evidence, validates expected behavior, documents issues, fixes discovered issues when appropriate, and reports results.

## Harness References
- Agent: `agents/evaluator.agent.md`
- Evals: `evals/`
- Runs: `runs/`
- Telemetry: `telemetry/run-log-schema.md`
