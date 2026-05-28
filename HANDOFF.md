# Project Handoff

## Last Updated

May 25, 2026 — after aligning core skills summary files, detailed command files (`plan.md`, `build.md`, `revise.md`, `prompt.md`, `run.md`, `new-project.md`), bootstrap scripts (`01`–`07`), reviewing specialized files (`plan-reviewer.md`, `e2e-test.md`), and adding explicit scope boundaries to `agents/builder.agent.md`. Harness validation passes 47/47 checks.

## Update — May 28, 2026

A consistency-and-coverage pass was completed. Validation still passes 47/47. This update supersedes the "Important Notes" and "Recommended Next Steps" sections below where they overlap.

**Fixed (the big one):** Stage contracts `01`–`03` were stale — they still described the old `Research / Draft / Review` content workflow even though the directories had been renamed. They are now rewritten as **Task Definition**, **Agent Design**, and **Prompt Design**, matching the `CONTEXT.md` routing table and the style of stages `04`–`07`. (`scripts/04-write-stage-contracts.sh` only copies these files, so the fix propagates to newly bootstrapped projects.)

**Cleanup / reconciliation:**
- Stale stage outputs and the old calculator demo moved to `archive/legacy-stage-outputs/`; stage `01`–`03` `output/` folders now match the empty `.gitkeep` pattern of `04`–`07`.
- Legacy docs archived to `archive/legacy-docs/`: `FINAL_SUMMARY.md`, `INITIAL.md`, `VERSION2.md`, `ICM-Framework-Tutorial.docx`. See `archive/README.md`.
- Deleted junk: `VERSION2.md.backup`, `skills/validate/SKILL.md.backup`, a checked-in `.pyc`, and `.DS_Store` files.

**Eval coverage / telemetry:**
- Added eval cases: `evals/cases/{prompt-design,code-review,tool-safety,agent-handoff,debugging}/`.
- Added `evals/results/_TEMPLATE-model-comparison.md` and example run records under `runs/examples/`.

**Skill refinement (harness-native):**
- `skills/plan/plan-reviewer.md` reframed from PRP-only to reviewing any harness artifact (Reviewer Agent), keeping the tool-schema/state-machine structure.
- `skills/tests/e2e-test.md` now has Mode A (app/browser E2E) and Mode B (harness artifact testing against rubrics, results to `evals/results/` + `runs/`).
- `skills/commit/gitcommit.md` gained Stage 07 Release context (eval preconditions, run records, `configs/tools.yaml` approvals).

**Tracking:** This project is now in Archon as **AI Agent Development Harness (_ICM-Template)** with a seeded task backlog.

**Also resolved this session:**
- `skills/ICM-README.md` and `skills/BUILD-README.md` were archived — both described a PRP slash-command flow and `.commands/`/`sync-commands.sh` infrastructure that does not exist in this repo. See `archive/legacy-docs/`.
- The repo is now a **git repository** with a baseline commit. A `.gitignore` excludes `node_modules/`, `.gitnexus/`, `__pycache__/`, and `.DS_Store`.

**Remaining follow-ups:**
- None blocking. Future work is tracked as Archon tasks (see project "AI Agent Development Harness (_ICM-Template)").

## Current State

This repository has been revised from a three-stage ICM content/workflow template into a plain-text, model-agnostic AI agent/model development harness.

The harness now supports designing, implementing, evaluating, iterating, and releasing agent/model workflows using explicit framework layers:

- Agents
- Skills
- Prompts
- Models
- Configs
- Evals
- Runs
- Telemetry
- Lifecycle stages

## Key Files to Read First

1. `README.md` — High-level project overview and workflow.
2. `FRAMEWORK.md` — Conceptual model for agents, skills, prompts, model profiles, evals, and runs.
3. `CLAUDE.md` — Assistant operating instructions.
4. `CONTEXT.md` — Routing table for lifecycle stages.
5. `VERSION3.md` — Primary alignment plan for the AI Agent Development Harness.
6. `archive/legacy-docs/VERSION2.md` — Legacy ICM alignment notes (archived, for historical reference).
7. `scripts/07-validate-harness.sh` — Structural validation script.

## Major Structural Additions

### Agent Layer

- `agents/README.md`
- `agents/researcher.agent.md`
- `agents/planner.agent.md`
- `agents/builder.agent.md`
- `agents/reviewer.agent.md`
- `agents/evaluator.agent.md`

### Prompt Layer

- `prompts/registry.md`
- `prompts/planner/v1.md`
- `prompts/planner/changelog.md`
- `prompts/reviewer/v1.md`
- `prompts/reviewer/changelog.md`

### Model and Config Layer

- `models/providers.md`
- `models/model-matrix.md`
- `models/local-models.md`
- `configs/agents.yaml`
- `configs/models.yaml`
- `configs/routing.yaml`
- `configs/tools.yaml`

### Evaluation Layer

- `evals/README.md`
- `evals/rubrics/plan-quality.md`
- `evals/rubrics/tool-safety.md`
- `evals/rubrics/agent-output-quality.md`
- `evals/cases/planning/basic-feature-plan.md`
- `evals/results/.gitkeep`

### Runs and Telemetry

- `runs/.gitkeep`
- `telemetry/README.md`
- `telemetry/run-log-schema.md`

### Lifecycle Stages

The old stages:

```text
01-research → 02-draft → 03-review
```

were replaced with:

```text
01-task-definition → 02-agent-design → 03-prompt-design → 04-tool-integration → 05-evaluation → 06-iteration → 07-release
```

Each stage has a `CONTEXT.md` contract.

## Skills Alignment Completed

The core `skills/*/SKILL.md` summary files and key detailed command files were updated to reference the new harness concepts.

### Builder Agent Scope Updated

- `agents/builder.agent.md` now includes an explicit **IN SCOPE** / **OUT OF SCOPE** section, making it clear the builder may act autonomously on implementation and plan updates while still requiring approval for commits, dependency installs, destructive commands, and unrelated changes.

Updated summary files include:

- `skills/plan/SKILL.md` now references Planner Agent, planner prompt, agent config, plan-quality eval, and stage 01.
- `skills/build/SKILL.md` now references Builder Agent, tool policy, and release stage.
- `skills/validate/SKILL.md` now references harness validation, evals, runs, and telemetry.
- `skills/tests/SKILL.md` now references Evaluator Agent, evals, runs, telemetry, and stage 05.
- `skills/run/SKILL.md` now supports approved runtime targets and harness workflows.
- `skills/commit/SKILL.md` now maps to Stage 07 Release, tool policy, and run-log schema.
- `skills/prompt/SKILL.md` now saves to `prompts/` and references prompt-design stage and evals.

Updated detailed command files include:

- `skills/plan/plan.md` now creates harness-aware plans for agents, prompts, skills, evals, models, configs, scripts, docs, and framework changes. It includes Harness References, Harness Context, Safety and Tooling Notes, Open Questions, and Recommended Next Agent fields.
- `skills/build/build.md` now uses Builder Agent framing, supports plans or PRPs, avoids automatic commits, and validates harness, code, scripts, prompts, agents, models, and evals.
- `skills/revise/revise.md` now supports revising plans, prompts, skills, agents, model profiles, configs, evals, stages, scripts, code, and docs based on validation or eval findings.
- `skills/prompt/prompt.md` now creates one-off prompts under `prompts/one-off/` or reusable prompt versions under `prompts/<name>/vN.md`.
- `skills/run/run.md` now starts approved runtime targets, demos, harness workflows, or eval targets while following `configs/tools.yaml`.
- `skills/new-project.md` now describes creating an agent harness project via `scripts/01-create-project.sh`.

## Bootstrap Scripts Alignment Completed

The scripts were updated so newly generated projects now use the agent harness structure.

Updated scripts:

- `scripts/01-create-project.sh`
  - Creates a full agent harness project by copying canonical files/folders from this template.
  - Customizes the generated `CLAUDE.md` title.
  - Runs validation after creation.

- `scripts/02-customize-claude.sh`
  - Writes a harness-oriented `CLAUDE.md`.

- `scripts/03-setup-routing.sh`
  - Writes the seven-stage agent harness routing table.

- `scripts/04-write-stage-contracts.sh`
  - Refreshes the seven lifecycle stage contracts from the template.

- `scripts/05-configure-brand-voice.sh`
  - Repurposed into a project profile configurator.
  - Writes `_config/project-profile.md`.
  - Keeps `_config/brand-voice.md` as a compatibility fallback if missing.

- `scripts/06-validate-workspace.sh`
  - Delegates to `scripts/07-validate-harness.sh`.

- `scripts/07-validate-harness.sh`
  - Validates either the template repo or a generated project via `PROJECT_ROOT`.

## Validation Performed

The following validation passed:

```bash
bash -n scripts/*.sh
scripts/07-validate-harness.sh
```

A stale-reference scan also passed for active skill files, excluding legacy backup files. The scan checked for old stage names (`01-research`, `02-draft`, `03-review`), old PRP prompt paths (`PRPs/prompts`), CRE8 workflow references, and journal-only workflow remnants across all `skills/*/*.md` files.

Harness validation result:

```text
Passed:   47
Warnings: 0
Failed:   0
```

An end-to-end smoke test was also run:

1. Generated a temporary project under `/tmp` using `scripts/01-create-project.sh`.
2. Ran the generated project’s `scripts/07-validate-harness.sh`.
3. Removed the temporary project.

Smoke test result:

```text
Passed:   47
Warnings: 0
Failed:   0
```

## Important Notes

- This folder is not currently a git repository, so no git diff or commit was created.
- Archon was referenced in global user rules, but no Archon files, commands, or project metadata were found in this workspace.
- `ICM-Framework-Tutorial.docx`, `INITIAL.md`, `FINAL_SUMMARY.md`, and `VERSION2.md.backup` may still reflect the older ICM/content-template era.
- `skills/validate/SKILL.md.backup` remains as a legacy backup and still contains older context-engineering template language.
- `skills/plan/plan-reviewer.md` was reviewed in detail. It is a comprehensive Reviewer Agent specification with JSON tool schemas, state machines, and workflow phases, but it is still heavily PRP-centric (e.g., "Validate PRPs Before Implementation", exit strategy references `/build PRPs/<feature>.md`). It would benefit from being reframed as a harness artifact review tool that checks agent contracts, prompt versions, eval rubrics, model profiles, configs, and tool policies.
- `skills/tests/e2e-test.md` was reviewed in detail. It is a comprehensive browser-based end-to-end testing skill using `agent-browser`, parallel sub-agents, and database validation. It is very application-centric (frontend, backend, database schemas) and would benefit from harness-specific additions: evaluating agent outputs against rubrics, testing prompt-version behavior, validating config changes, and recording results to `evals/results/` and `runs/` instead of only `e2e-screenshots/`.
- `skills/commit/gitcommit.md` still references conventional git commit workflows without harness-specific release-stage context (e.g., no mention of `stages/07-release/`, run records, or eval preconditions).
- Re-run `scripts/07-validate-harness.sh` after any changes to confirm structural validation still passes.

## Recommended Next Steps

### 1. Deep-refine remaining specialized skill files

The main stale references have been removed from active skill files, and Harness References have been added to `skills/plan/SKILL.md`, `skills/tests/SKILL.md`, `skills/commit/SKILL.md`, and `skills/plan/plan.md`. Remaining files to review for deeper harness consistency:

- `skills/plan/plan-reviewer.md`
- `skills/tests/e2e-test.md`
- `skills/commit/gitcommit.md`
- `skills/validate/SKILL.md.backup` if backup cleanup is desired

Goal: make each command fully consistent with agent contracts, stage contracts, evals, model profiles, run records, and tool safety policy.

### 2. Add more eval cases

Current eval coverage is minimal. Add cases for:

- Prompt design
- Code review
- Tool safety
- Agent handoff quality
- Model comparison
- Debugging/refactoring workflows

### 3. Add run examples

Create example run records under `runs/examples/` or `runs/` using `telemetry/run-log-schema.md`.

### 4. Decide what to do with legacy files

Review older files and either revise, archive, or remove them:

- `FINAL_SUMMARY.md`
- `INITIAL.md`
- `VERSION2.md.backup`
- `ICM-Framework-Tutorial.docx`

### 5. Consider initializing git

If version control is desired, initialize git and commit the harness baseline after reviewing the generated files.

## Suggested Next Agent Prompt

```text
You are taking over the /Users/james/Projects/_ICM-Template project. Read HANDOFF.md, README.md, FRAMEWORK.md, CLAUDE.md, CONTEXT.md, and VERSION3.md first. The repo is a plain-text, model-agnostic AI agent/model development harness. Validation currently passes with scripts/07-validate-harness.sh. Core skills, detailed commands, and bootstrap scripts have been aligned. Harness References have been added to skills/plan/SKILL.md, skills/tests/SKILL.md, skills/commit/SKILL.md, and skills/plan/plan.md. Continue by deep-refining remaining specialized skill files (skills/plan/plan-reviewer.md, skills/tests/e2e-test.md, skills/commit/gitcommit.md), then add more eval cases and run examples.
```
