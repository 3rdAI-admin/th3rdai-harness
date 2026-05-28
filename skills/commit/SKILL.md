# Skill: gitcommit

Invoked by: /gitcommit command

## Purpose
Review local changes, prepare an accurate commit message and optional changelog summary, and commit only changes explicitly approved by the user.

## When to Use
- When file changes are ready to be committed
- After implementation, validation, or documentation updates
- Before pushing to remote
- When asked to summarize and commit current work
- During `stages/07-release/` after validation and review are complete

## Output
Creates an approved git commit with a clear message, concise change summary, validation notes, and any follow-up risks.

## Harness References
- Stage: `stages/07-release/`
- Tool policy: `configs/tools.yaml`
- Run log schema: `telemetry/run-log-schema.md`

## Next Step
Review `git status` and `git diff`, confirm the intended files and commit message, then run the approved commit.

## Related Skill: revise

Invoked by: /revise command

### Purpose
Revise a plan, prompt, skill, agent, model profile, config, or eval when validation reveals design-level issues.

### When to Use
- When build or validation fails because the plan is wrong
- When missing implementation steps are discovered
- When the technical approach needs correction
- When eval results require iteration before release

### Output
Updates the relevant artifact or plan with the revised approach.

### Next Step
Re-run `/build`, `/validate`, or the relevant eval with the revised artifact.
