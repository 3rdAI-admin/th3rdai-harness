# Stage 07: Release

## Purpose

Prepare a stable agent, prompt, skill, model profile, eval, config, or framework update for use, documentation, or commit.

## Token Budget

**Estimated context cost:** ~8K-13K tokens

**Breakdown:**
- Reviewer agent contract (~1K tokens)
- Release skill (~800 tokens)
- This stage context (~500 tokens)
- Changed artifacts for review (~3K-6K tokens)
- Evaluation results (~1.5K-2K tokens)
- Changelogs (~1K tokens)
- skills/commit/gitcommit.md (~800 tokens)
- skills/security/security.md (if security review needed) (~2K tokens)
- telemetry/run-log-schema.md (~500 tokens)

**Variance drivers:** Number and size of changed files, whether security review required, extent of evaluation evidence, whether release notes or git commit needed.

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
