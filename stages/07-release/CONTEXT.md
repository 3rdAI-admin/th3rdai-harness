# Stage 07: Release

## Purpose

Prepare a stable agent, prompt, skill, model profile, eval, config, or framework update for use, documentation, or commit.

## Inputs

| File | Load | Reason |
|------|------|--------|
| Changed artifacts | Full | Verify release contents |
| Evaluation results | Full if present | Confirm quality evidence |
| Relevant changelogs | Full | Ensure history is documented |
| `skills/commit/gitcommit.md` | Full if committing | Follow safe commit process |
| `skills/security/security.md` | Targeted if auth/API/security headers changed | Web security diff review or threat-model gate |
| `telemetry/run-log-schema.md` | Targeted | Record final run metadata |

## Process

1. Confirm the release scope and changed files.
2. Verify required docs, registries, changelogs, configs, and eval results are updated.
3. Check for unresolved high-risk issues.
4. Run appropriate validation.
5. Summarize what changed, why it changed, and how it was validated.
6. If committing, use the safe git commit workflow and ask for approval before staging or committing.

## Outputs

| File | Location | Format |
|------|----------|--------|
| Release notes | `output/release-notes.md` | Markdown |
| Run record | `runs/<run-id>.md` | Markdown or YAML when useful |
| Commit | Git history | Only with explicit approval |

## Checkpoint

Do not release if required validation is missing, high-risk findings are unresolved, or the changed file set is unclear.
