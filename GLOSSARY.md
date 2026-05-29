# Glossary

Quick-reference definitions for the harness. See `FRAMEWORK.md` for the conceptual model and `CONTEXT.md` for routing.

## Core Concepts

| Term | Definition | Lives in |
|------|------------|----------|
| **Agent** | A role-based actor with permissions, inputs, outputs, success criteria, and handoff rules. Answers *who does the work?* | `agents/*.agent.md` |
| **Skill** | A reusable procedure an agent follows. Answers *how is the work done?* Each skill has a `SKILL.md` summary and a detailed command file. | `skills/<name>/` |
| **Prompt** | A versioned instruction template used by an agent or skill. Answers *what exact instruction pattern is reused or tested?* Never overwrite a version; add `vN`. | `prompts/<name>/vN.md` |
| **Model Profile** | Provider/model settings bound to an agent. Answers *which model runs this work, under what settings?* | `configs/models.yaml` |
| **Evaluation** | A repeatable rubric, case, or result that measures performance. Answers *how do we know it worked?* | `evals/` |
| **Run** | A recorded execution of an agent, skill, prompt, or eval. Answers *what happened, with which inputs and outputs?* | `runs/`, schema in `telemetry/run-log-schema.md` |
| **Stage** | A lifecycle phase with an input/output contract. | `stages/NN-*/CONTEXT.md` |
| **Config** | Machine-readable agent, model, routing, and tool policies. | `configs/*.yaml` |

## Skill File Convention

| File | Role |
|------|------|
| `skills/<name>/SKILL.md` | Short summary: purpose, when to use, output, harness references, and a **Procedure** link to the detailed file. |
| `skills/<name>/<name>.md` | The executable procedure the agent follows (process, safety notes, examples, success criteria). |

A skill is wired to an agent through `configs/agents.yaml` (`default_skill`). The detailed file is the source of truth the agent loads.

## Agents and Their Skills

| Agent | Default Skill | Prompt | Model Profile |
|-------|---------------|--------|---------------|
| Researcher | `skills/research/research.md` | `prompts/researcher/v1.md` | `research` |
| Planner | `skills/plan/planner.md` | `prompts/planner/v1.md` | `planning` |
| Builder | `skills/build/build.md` | `prompts/builder/v1.md` | `building` |
| Reviewer | `skills/plan/plan-reviewer.md` | `prompts/reviewer/v1.md` | `review` |
| Evaluator | `skills/eval/eval.md` | `prompts/evaluator/v1.md` | `evaluation` |

## Lifecycle

```text
Task Definition → Agent Design → Prompt Design → Tool Integration → Evaluation → Iteration → Release
   (01)              (02)            (03)             (04)              (05)         (06)        (07)
```

## Commands

| Command | Skill | Purpose |
|---------|-------|---------|
| `/research` | `skills/research/` | Gather grounded context before planning |
| `/plan` | `skills/plan/` (planner) | Create an implementation-ready plan |
| `/plan-reviewer` | `skills/plan/` (reviewer) | Review a plan or harness artifact |
| `/build` | `skills/build/` | Implement an approved plan within scope |
| `/eval` | `skills/eval/` | Score an artifact against a rubric |
| `/validate` | `skills/validate/` | Run harness, structure, and artifact checks |
| `/debug` | `skills/debug/` | Diagnose a failure and propose a minimal fix |
| `/revise` | `skills/revise/` | Fix a plan or artifact after a finding |
| `/prompt` | `skills/prompt/` | Create a one-off or versioned prompt |
| `/run` | `skills/run/` | Start an approved runtime target |
| `/tests/e2e-test.md` | `skills/tests/` | Run end-to-end or harness-case testing |
| `/gitcommit` | `skills/commit/` | Prepare a reviewed commit (Stage 07) |
