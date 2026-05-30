# Project Notes (deployment overlay)

This file captures project-specific paths, commands, and shortcuts that generic harness
skills reference but don't embed directly. When bootstrapping a new project from the
harness template:

1. Copy this file to `_config/project-notes.md` (or rename if already at that path)
2. Replace all `<placeholders>` with your project's actual values
3. Delete sections that don't apply to your project (e.g., orchestrator if not using it)
4. Commit the filled-in `project-notes.md` to your project repo

Generic harness skills will reference this file when it exists, allowing them to remain
portable across projects.

## Project

**Name:** `<your-project-name>`
**Tracking:** `<issue tracker URL or Archon project ID, if using Archon MCP>`
**Repo:** `<GitHub/GitLab URL or local path>`

## Resume (read first when returning)

When starting a new session or handing off to another agent:

1. Read `<HANDOFF.md or README.md or similar>` first
2. Check `<alignment doc, project status doc, or VERSION.md, if any>`
3. Verify tests pass (see "Verify green" below)
4. Check tracking system for active tasks (see "Tracking" above)

## Verify green (this project)

Always run these before committing changes:

```bash
# Harness structural validation (if using harness framework)
scripts/07-validate-harness.sh

# Project-specific tests - uncomment and customize:
# npm test
# pytest
# python3 -m unittest discover
# cargo test
# go test ./...

# Orchestrator tests (if Phase 01-04 implemented):
# python3 -m unittest discover scripts/orchestrator/tests
```

**Important:** Record actual Passed/Failed counts from script output in commit messages
or tracking system — do not hardcode expected check counts in skills, as they change
when the project evolves.

## Optional tooling (if present)

List optional scripts, CLIs, or subsystems that exist **only in some deployments**.
This helps agents understand what's available without assuming all harness features
are present:

### Native Orchestrator (if implemented)
- **Entry point:** `scripts/orchestrate.py` (if exists)
- **Verify:** `python3 scripts/orchestrate.py --help`
- **Docs:** `plans/native-orchestrator/EFFORT.md`
- **Config:** `configs/routing.yaml` for available routes

### Other Custom Tools
- **Name:** `<tool name>`
- **Path:** `<path to script or CLI>`
- **Verify:** `<command to test it works>`
- **Docs:** `<path to documentation>`

## Research shortcuts

Quick paths to key information for research and planning tasks:

- **Agent contracts:** `agents/` (role definitions, permissions, handoffs)
- **Skills:** `skills/` (reusable procedures organized by function)
- **Prompts:** `prompts/` (versioned prompt templates)
- **Configs:** `configs/` (agent, model, routing, tool policies)
- **Stage contracts:** `stages/` (lifecycle stage definitions and flows)
- **Plans:** `plans/` (implementation-ready plans and effort trackers)
- **Evals:** `evals/` (rubrics, cases, results)
- **Domain docs:** `<path to domain/business context docs, if any>`
- **API specs:** `<path to API documentation, if any>`

## Debug shortcuts

Common issues and how to reproduce/diagnose them:

| Symptom | Likely repro | Fix |
|---------|--------------|-----|
| Import errors in orchestrator | `python3 -c "from scripts.orchestrator import config"` | Run from repo root; check PYTHONPATH |
| Validator fails | `scripts/07-validate-harness.sh` | Check output for missing files or broken references |
| Tests fail after config change | `<your test command>` | Verify config syntax; check for typos |
| `<project-specific symptom>` | `<reproduce command>` | `<typical fix>` |

## Run skill (optional route driver)

If `scripts/orchestrate.py` exists (Native Orchestrator Phase 01-04 implemented),
document usage here:

### Available Routes
Check `configs/routing.yaml` for the complete list. Common routes:
- `task_definition` - Stage 01 (research → plan)
- `agent_design` - Stage 02 (plan → review)
- `prompt_design` - Stage 03 (plan → review)
- `evaluation` - Stage 05 (evaluate → review)
- `iteration` - Stage 06 (plan → build → evaluate)

### Dry-run (default, safe)
```bash
# Assemble context bundles and write run records, no model invocation
python3 scripts/orchestrate.py route <route-name>
python3 scripts/orchestrate.py route task_definition  # example

# Run records written to: runs/YYYYMMDD-HHMMSS-<route>-<step>-<agent>.md
```

### Execute mode (opt-in, Phase 04)
```bash
# Actually invoke agent CLI (requires configs/execution.yaml configured)
python3 scripts/orchestrate.py route <route-name> --execute --adapter cli --max-steps N

# Checkpoints: default is per-step approval; add --yes to skip checkpoints
# (but approval gates from configs/tools.yaml ALWAYS apply, even with --yes)

# Example with checkpoint bypass:
python3 scripts/orchestrate.py route task_definition --execute --adapter cli --max-steps 1 --yes
```

### Approval Gates
Per `configs/tools.yaml`, these actions **always** require approval:
- `git commit` / `git push` / `git merge`
- `npm install` / `pip install` / package installs
- `rm -rf` / destructive file operations
- Network/API calls (depending on policy)

Even `--yes` flag does **not** bypass these gates.

## Eval skill (optional CLI scaffold)

If an eval subcommand exists on the project CLI (e.g., orchestrator has `eval` subcommand),
document it here:

### Orchestrator Eval Scaffold (if Phase 03 implemented)
```bash
# Generate eval result markdown from a case file
python3 scripts/orchestrate.py eval evals/cases/<category>/<case-name>.md

# Example:
python3 scripts/orchestrate.py eval evals/cases/orchestrator/config-subset-parsing.md

# Produces: evals/results/YYYYMMDD-<case-name>-result.md (template to fill in)
```

### Manual Eval Flow (always available)
1. Select case from `evals/cases/`
2. Run the test/task described in the case
3. Score against the rubric referenced in the case
4. Record results in `evals/results/` with timestamp prefix

## Plan / build / release notes

### Planning
- **Plans:** `plans/` directory (implementation-ready plans)
- **Effort tracking:** `<path to EFFORT.md or similar, if used>`
- **Multi-phase efforts:** Organize as `plans/<feature-name>/` with phase subdocs

### Build
- **Pre-build:** Run validator and tests (see "Verify green" above)
- **Build command:** `<your build command, e.g., npm run build, cargo build, go build>`
- **Build artifacts:** `<where build outputs go>`

### Release
- **Pre-commit:** Verify eval results pass (check `evals/results/`)
- **Pre-release:** Confirm rubrics score above pass threshold for critical cases
- **Release process:** Follow `stages/07-release/README.md`
- **Approval required:** Commits need explicit human approval per `CLAUDE.md`

## Open decisions

Track unresolved design decisions and who owns them:

- **Decision:** `<what needs to be decided>`
  - **Owner:** `<who decides>`
  - **Context:** `<why this matters>`
  - **Options:** `<A, B, C...>`
  - **Deadline:** `<when decision is needed>`

## Bootstrap Checklist

When setting up this file for a new project:

- [ ] Replace project name, tracking, repo URL
- [ ] Update "Resume" section with actual handoff docs
- [ ] Configure "Verify green" commands for your stack
- [ ] Document any optional tooling (orchestrator, custom CLIs)
- [ ] Fill in research shortcuts with actual paths
- [ ] Add project-specific debug shortcuts
- [ ] Configure run/eval sections if using orchestrator
- [ ] Document build/release process
- [ ] List any open decisions
- [ ] Delete this checklist section
- [ ] Commit as `_config/project-notes.md` to your repo
