---
description: Review local git changes and create an approved commit
---

# Git Commit - Review Changes and Commit Safely

Create a git commit only after reviewing the current changes, drafting an accurate message, and getting user confirmation.

## Harness Context

This skill implements the commit step of **Stage 07: Release** (`stages/07-release/`). Deployment-specific release checks may be listed in `_config/project-notes.md`.

Before committing a harness artifact (agent, prompt, skill, model profile, eval, config, or framework change):

- Confirm any required evaluation has run and is not failing — do not release on unresolved blocking eval failures (`evals/results/`).
- Confirm changelogs and registries are updated (e.g., `prompts/<name>/changelog.md`, `prompts/registry.md`).
- Follow the approval rules in `configs/tools.yaml`: staging, committing, and pushing always require explicit user approval; never force-push to main.
- When the change is significant, record a run per `telemetry/run-log-schema.md` under `runs/`.

## Input: $ARGUMENTS
- Optional commit message, changelog notes, file paths, or scope hints

## Process

### 1. Inspect Repository State
- Run `git status --short` to identify changed, staged, untracked, and deleted files
- Run `git diff --stat` to summarize unstaged changes
- Run `git diff --cached --stat` to summarize staged changes
- If the current directory is not a git repository, stop and report that no commit can be made

### 2. Review Changes
- Review diffs for files that appear relevant to the requested commit
- Check for unintended changes, debug artifacts, secrets, generated files, or unrelated edits
- If unrelated changes are present, ask which files should be included before staging or committing
- Do not read `.env` files or expose secret values

### 3. Prepare Commit Content
- Draft a concise commit message that reflects the actual changes
- Prefer an imperative subject line, such as `Fix plan skill output format`
- Include a short body when the changes need context, validation notes, or follow-up details
- If requested, prepare changelog notes grouped by area changed

### 4. Confirm Before Mutating Git State
Before staging or committing, present:
- Files intended for the commit
- Commit message
- Optional commit body or changelog notes
- Evaluation status for any harness artifact being released (passed / not run / failing)
- Any risks, skipped files, or unresolved questions

Ask for explicit approval before running `git add` or `git commit`.

### 5. Commit Approved Changes
- Stage only the approved files
- Run `git commit` with the approved message
- If there are no changes to commit, stop and report that the working tree is clean
- If commit hooks fail, report the failure output and do not bypass hooks unless the user explicitly requests it

### 6. Output
Report:
- Commit hash if created
- Commit message used
- Files committed
- Any files left uncommitted
- Suggested next step, such as pushing or continuing work

## Example Usage
```
/gitcommit
/gitcommit "Fix e2e test skill safety instructions"
/gitcommit skills/plan skills/tests
```

## Success
When complete, report the created commit and suggest reviewing `git status` before pushing.
