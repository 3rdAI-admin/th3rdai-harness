---
description: Score a harness artifact against a rubric and record the result
name: eval
---

# Eval - Score a Harness Artifact Against a Rubric

Loaded by `/eval` via `skills/eval/SKILL.md` and `configs/agents.yaml` (`evaluator.default_skill`).

Use the Evaluator Agent to measure whether an agent, prompt, skill, or model profile performs well enough to use or release. This skill implements the evaluation flow described in `evals/README.md`.

## Harness References

- Agent: `agents/evaluator.agent.md`
- Rubrics: `evals/rubrics/`
- Cases: `evals/cases/`
- Results: `evals/results/`
- Registry: `evals/README.md`
- Telemetry: `telemetry/run-log-schema.md`
- Stage: `stages/05-evaluation/`
- Deployment overlay (optional): `_config/project-notes.md`

## Input: $ARGUMENTS

- The artifact under evaluation (e.g. `prompts/planner/v1.md`, `agents/reviewer.agent.md`, a skill, or a `model_profile` name)
- Optional: a specific eval case path and rubric path. If omitted, select the most relevant case from `evals/cases/` and rubric from `evals/rubrics/`.

## Process

### 1. Fix the Evaluation Setup

Record these before producing any output, and do not change them mid-run:

```markdown
## Evaluation Setup
- Artifact under test: <path or profile name>
- Eval case: <evals/cases/.../case.md>
- Rubric: <evals/rubrics/....md>
- Model profile: <profile name or TBD>
- Prompt version: <prompts/.../vN.md or n/a>
```

### 2. Produce or Collect the Output

- Run the artifact against the case input, or use a captured output supplied by the user.
- Do not modify the artifact while evaluating it.
- Keep the rubric stable. If the rubric is wrong, stop and revise the rubric in a separate step, then restart the run.

### 3. Score Against the Rubric

For each rubric criterion, record a score and a one-line justification tied to evidence in the output:

```markdown
## Scores
| Criterion | Score | Justification (cite output) |
|-----------|-------|-----------------------------|
| <criterion> | <score> | <evidence> |

Total: <aggregate> / <max>
```

### 4. Failure Analysis

```markdown
## Findings
- severity: high|medium|low
  observation: <what the output did or missed>
  rubric_link: <which criterion>
  recommendation: <specific revision>
```

Separate observations (what happened) from recommendations (what to change). Never hide a failed result.

### 5. Record the Result

Save an evaluation record to `evals/results/<run-id>.md` and a run record per `telemetry/run-log-schema.md`:

```yaml
run_id: YYYYMMDD-HHMMSS-short-name
agent: evaluator
skill: skills/eval/eval.md
prompt_version: <optional>
model_profile: <optional>
inputs:
  - <case path>
outputs:
  - evals/results/<run-id>.md
evaluation:
  rubric: <rubric path>
  score: <aggregate>
  notes: <summary>
issues:
  - severity: <high|medium|low>
    description: <summary>
follow_up:
  - <next action>
```

### 6. Output

```text
EVAL COMPLETE: <artifact under test>

Case:   <case path>
Rubric: <rubric path>
Score:  <aggregate> / <max>

Verdict: acceptable | needs revision | reject

Top findings:
- <finding>

Next:
- Acceptable -> stages/07-release/
- Needs revision -> /revise <artifact> "<finding>" then re-run /eval
```

## Optional eval scaffolding

Some deployments include a CLI that pairs a case with its rubric and writes **PENDING** result/run stubs (Evaluator still scores manually). If `scripts/orchestrate.py` exists, see `_config/project-notes.md` for the eval subcommand; otherwise use `/eval` only.

## Safety and Tooling Notes

- Read-only by default; run only approved commands per `configs/tools.yaml`.
- Do not change production behavior while evaluating.
- If the rubric must change, record the change and re-run from a clean setup — never edit a rubric after seeing results to make a failing artifact pass.

## Example Usage

```text
/eval prompts/planner/v1.md
/eval prompts/planner/v1.md evals/cases/planning/basic-feature-plan.md
/eval agents/reviewer.agent.md "compare against evals/rubrics/agent-output-quality.md"
/eval "model_profile: planning vs building on basic-feature-plan"
```

## Success Criteria

- The evaluation setup is fixed and recorded before scoring.
- Every score maps to a rubric criterion and cites evidence.
- Results are repeatable and saved to `evals/results/` and `runs/`.
- Recommendations are specific and actionable.
