# Project Notes (deployment overlay)

Replace this file per project. Copy to `project-notes.md` when bootstrapping, or edit
`project-notes.md` directly. Generic harness skills do **not** embed application-specific
paths here — they only point agents to this file when it exists.

## Project

**Name:** <project name>  
**Tracking:** <issue tracker / Archon project id, if any>

## Resume (read first when returning)

1. <handoff or README path>
2. <alignment doc, if any>

## Verify green (this project)

```bash
scripts/07-validate-harness.sh
# Add project-specific tests below, e.g.:
# npm test
# pytest
```

Record actual Passed/Failed from script output — do not hardcode check counts in skills.

## Optional tooling (if present)

List optional scripts, CLIs, or subsystems that exist **only in some deployments**:

- Path: `<path>`
- Verify: `<command>`
- Docs: `<path>`

## Research shortcuts

- <where to find routing, configs, or domain docs>

## Debug shortcuts

| Symptom | Likely repro |
|---------|----------------|
| <symptom> | `<command>` |

## Run skill (optional route driver)

If `scripts/orchestrate.py` exists, document dry-run vs `--execute` commands, adapters, and approval gates here.

## Eval skill (optional CLI scaffold)

If an eval subcommand exists on the project CLI, document it here.

## Plan / build / release notes

- <where plans live, effort trackers, post-build checks, pre-commit eval requirements>

## Open decisions

- <decision awaiting owner>
