---
description: Build - Implement an approved plan and validate the result
tools: Read, TodoWrite, TodoRead, Write, MultiEdit, Crawl, Grep, Bash
---

# /build - Implement and Validate

Use the Builder Agent to implement an approved plan or PRP, validate the result, and summarize changes.

## Harness References

- Agent: `agents/builder.agent.md`
- Stage: `stages/04-tool-integration/`, `stages/06-iteration/`, or `stages/07-release/`
- Tool policy: `configs/tools.yaml`
- Validation: `skills/validate/validate.md`
- Telemetry: `telemetry/run-log-schema.md`
- Deployment overlay (optional): `_config/project-notes.md`

## Usage

```text
/build
/build plans/my-change.md
/build PRPs/my-feature.md
```

## What This Does

1. Finalize the approved plan or PRP.
2. Create an implementation task list.
3. Implement approved changes only.
4. Validate with relevant checks.
5. Summarize files changed, validation results, risks, and next steps.

## Step 1: Load Plan

{{if $ARGUMENTS}}
  Read file: $ARGUMENTS
{{else}}
  Look for candidate files in `plans/` and `PRPs/`.
  Ask user: "Which plan should be built?"
  Wait for user selection.
{{endif}}

If no plan exists, suggest `/plan <request>` first.

## Step 2: Confirm Scope

Present a short summary:

- Goal
- Artifact type: code, agent, prompt, skill, eval, model profile, config, script, docs, or framework
- Key implementation steps
- Files expected to change
- Validation criteria
- Safety/tooling risks

Ask: "Proceed with implementation, or revise first?"

- If revise: route to `/revise <plan-path>`.
- If proceed: continue to implementation.

## Step 3: Create Task Plan

Create a task list from the approved implementation steps.

Before writing files:

- Read relevant existing files.
- Identify repository conventions from `CLAUDE.md`, `FRAMEWORK.md`, and nearby files.
- Confirm imports, dependencies, generated files, and tool permissions.
- Do not install dependencies, delete files, or mutate git state without explicit approval.

## Step 4: Implement

For each task:

1. Mark the task in progress.
2. Implement the smallest sufficient change.
3. Keep changes scoped to the approved plan.
4. Mark the task complete.
5. Record any deviation from the plan.

Do not create commits automatically. Use `/gitcommit` during release after explicit approval.

## Step 5: Validate

Run validation based on the artifact type.

### Harness Changes

```bash
scripts/07-validate-harness.sh
```

If `_config/project-notes.md` exists, also run any extra **Verify green** commands listed there (project-specific tests or optional CLIs).

### Shell Scripts

```bash
bash -n scripts/*.sh
```

### Python Projects

```bash
ruff check . 2>/dev/null || echo "ruff not installed, skipping"
mypy . 2>/dev/null || echo "mypy not installed, skipping"
pytest 2>/dev/null || echo "pytest not installed, skipping"
```

### TypeScript Projects

```bash
tsc --noEmit 2>/dev/null || echo "tsc not available, skipping"
npm test 2>/dev/null || echo "npm test not configured, skipping"
```

### Agent, Prompt, Model, or Eval Changes

- Check relevant contracts in `agents/`.
- Check prompt registry and changelogs.
- Check configs in `configs/`.
- Run or document relevant evals under `evals/`.
- Record useful evidence in `runs/`.

## Step 6: Summarize Results

Use this output format:

```text
BUILD COMPLETE: <name>

Files created/modified:
- <path> — <reason>

Validation results:
- <check>: passed|failed|skipped — <notes>

Risks and follow-up:
- <risk or none>

Next steps:
1. /validate
2. Run relevant evals
3. Move to stages/07-release/ when ready
```

## Error Handling

If validation fails:

1. Show specific errors.
2. Identify whether this is an implementation bug or plan/artifact issue.
3. Fix direct implementation bugs when safe.
4. Use `/revise <artifact>` when the plan, prompt, agent, config, eval, or model profile is wrong.
5. Re-run the failing validation.

If the plan is incomplete:

- Point out missing sections.
- Ask the user to revise or approve proceeding with known gaps.

## Success Criteria

- Approved plan was followed.
- All tasks are complete or explicitly deferred.
- Validation passes or skipped checks are explained.
- No unrelated files were changed.
- Summary includes next steps and remaining risks.
