# Skill: eval

Invoked by: /eval command

## Procedure

Load and follow `skills/eval/eval.md` when executing this skill.

## Purpose
Use the Evaluator Agent to score an agent, prompt, skill, or model profile against a rubric and a representative case, then record the result.

## When to Use
- During `stages/05-evaluation/`
- After a prompt, agent, skill, or config change that needs evidence before release
- When comparing two model profiles or prompt versions
- Before `stages/07-release/` to confirm quality is acceptable

## Output
Produces an evaluation result with rubric scores, rationale, failure analysis, and recommended revisions, saved to `evals/results/` and recorded as a run.

## Harness References
- Procedure: `skills/eval/eval.md`
- Agent: `agents/evaluator.agent.md`
- Rubrics: `evals/rubrics/`
- Cases: `evals/cases/`
- Results: `evals/results/`
- Config: `configs/agents.yaml`
- Telemetry: `telemetry/run-log-schema.md`

## Next Step
- Acceptable: proceed to `stages/07-release/`
- Issues found: run `/revise` with the findings, then re-run `/eval`
