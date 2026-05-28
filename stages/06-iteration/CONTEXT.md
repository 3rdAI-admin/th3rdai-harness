# Stage 06: Iteration

## Purpose

Improve agents, prompts, skills, model profiles, configs, or evaluations based on findings from review or evaluation.

## Inputs

| File | Load | Reason |
|------|------|--------|
| Evaluation findings | Full | Understand what failed or needs improvement |
| Review findings | Full if present | Incorporate reviewer feedback |
| Relevant artifact | Full | Revise the correct source |
| Relevant changelog | Full if present | Preserve version history |
| Relevant config | Targeted | Keep routing and model assumptions aligned |

## Process

1. Identify the failure, gap, or improvement target.
2. Determine whether to revise an agent, skill, prompt, model profile, eval, config, or script.
3. Make the smallest change that addresses the finding.
4. Update changelogs, registries, and config references.
5. Re-run or document the relevant evaluation path.
6. Record remaining risks and follow-up work.

## Outputs

| File | Location | Format |
|------|----------|--------|
| Revised artifact | Relevant folder | Markdown, YAML, shell, or code |
| Iteration notes | `output/iteration-notes.md` | Markdown |
| Updated results | `evals/results/` or `runs/` | Markdown or YAML |

## Checkpoint

If the iteration changes agent permissions, tool policies, or model routing, stop for review before release.
