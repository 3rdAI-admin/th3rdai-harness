# Archive

Historical artifacts preserved for reference. Nothing here is part of the active harness, and none of it is checked by `scripts/07-validate-harness.sh`.

## legacy-docs/

Documents from before the repository became an AI Agent Development Harness, or superseded by current docs:

| File | Why archived | Superseded by |
|------|--------------|---------------|
| `FINAL_SUMMARY.md` | Summarized the old "Simple Statistics Calculator" demo | `README.md`, `HANDOFF.md` |
| `INITIAL.md` | Original calculator project spec (content-template era) | `stages/01-task-definition/` |
| `VERSION2.md` | Migration notes for the ICM → harness transition | `VERSION3.md` |
| `ICM-Framework-Tutorial.docx` | Onboarding tutorial for the original ICM content template | `FRAMEWORK.md`, `README.md` |
| `ICM-README.md` | Old `skills/` README describing a PRP slash-command flow and example skills that no longer exist | `FRAMEWORK.md`, the actual `skills/<name>/SKILL.md` files |
| `BUILD-README.md` | Described a `.commands/` + `sync-commands.sh` multi-IDE distribution system that does not exist in this repo | n/a — superseded by the harness `skills/` layout |

## legacy-stage-outputs/

Sample outputs left over from the old three-stage content workflow (`research → draft → review`), removed when stages `01`–`03` were rewritten as Task Definition / Agent Design / Prompt Design. The `02-agent-design/` calculator demo is kept intact as a complete worked example of the original template.
