---
description: Revise a plan or harness artifact when validation fails
---

# Revise - Fix Plan or Harness Artifact Issues

Use `/revise` when `/build`, `/validate`, review, or evaluation reveals that the plan or source artifact is wrong, incomplete, unsafe, or misaligned with the harness.

## Harness References

- Stage: `stages/06-iteration/`
- Agents: `agents/planner.agent.md`, `agents/reviewer.agent.md`, `agents/evaluator.agent.md`
- Evals: `evals/`
- Runs: `runs/`
- Telemetry: `telemetry/run-log-schema.md`

## Input: $ARGUMENTS

- Path to a plan, PRP, prompt, agent contract, skill, config, eval, or model profile
- Description of what went wrong or what finding needs to be addressed

## When to Use Revise vs Fix

| Situation | Action |
|-----------|--------|
| Implementation has bugs, but approach is right | Fix implementation directly, re-run `/validate` |
| Wrong model, agent, prompt, tool policy, architecture, or missing steps | Use `/revise` to update the source artifact or plan |
| Validation reveals missing requirements | Use `/revise` to update the plan/artifact and validation criteria |
| Eval reveals behavior regression | Use `/revise` and record iteration notes |
| Tool safety issue is found | Revise `configs/tools.yaml`, the relevant skill, or the agent contract |

## Process

### 1. Load Context

- Read the target artifact
- Review `/validate`, `/build`, review, or eval output
- Read relevant run records from `runs/` if available
- Read relevant rubrics or cases from `evals/`

### 2. Analyze Failure

```markdown
## Failure Analysis

Original approach:
- <approach from artifact>

Finding observed:
- <what went wrong>

Root cause:
- <why it failed: missing context, wrong assumption, weak prompt, unsafe tool policy, bad model fit, missing eval, etc.>

Affected layer:
- <agent|skill|prompt|model|config|eval|stage|script|code|docs>
```

### 3. Update Artifact

Revise the relevant file with corrections:

```markdown
## Revised Approach
<new approach addressing the failure>

## Changes Made
- <what changed and why>
- <steps added, removed, or reordered>
- <evaluation or validation updates>

## Validation Criteria Updated
- [ ] <updated check>
- [ ] <new check for previous failure>
```

### 4. Record Iteration Evidence

When useful, save notes to:

- `stages/06-iteration/output/iteration-notes.md`
- `runs/<run-id>.md`
- `evals/results/<run-id>.md`

### 5. Output

```text
REVISION COMPLETE: <artifact path>

Changes made:
- <summary>

Validation to re-run:
- <checks/evals>

Next:
- Re-run `/build`, `/validate`, or the relevant eval.
```

## Example Usage

```text
/revise plans/reviewer-agent.md "tool permissions are too broad"
/revise prompts/planner/v1.md "plans consistently miss validation criteria"
/revise configs/models.yaml "local model fails planning eval"
/revise evals/rubrics/tool-safety.md "rubric does not cover git mutation"
```

## Success Criteria

- The artifact clearly identifies what went wrong
- Revised approach addresses root cause
- New validation criteria prevent regression
- Iteration evidence is recorded when useful
