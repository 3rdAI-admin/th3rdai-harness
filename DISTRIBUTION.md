# Harness Distribution Guide

This harness is distributed as a **copyable workspace template**, not as an npm or PyPI install. The value is plain-text contracts (agents, skills, prompts, configs, evals) that a capable AI agent or human drives — plus optional stdlib-only Python tooling under `scripts/orchestrator/`.

Choose the path that matches how you want to consume or ship the harness.

**New to the harness?** Start with **`TUTORIAL.md`** for a step-by-step walkthrough (new repo + existing app).

---

## Path A — GitHub template (recommended)

Best for: sharing the harness with a team, open-sourcing a starter, or publishing versioned releases.

### For consumers (start a new project from the template)

1. On GitHub, open the harness repository and click **Use this template** → **Create a new repository**.
2. Clone your new repo locally.
3. Customize deployment overlay:
   ```bash
   cp _config/project-notes.TEMPLATE.md _config/project-notes.md
   # Edit placeholders; delete sections that do not apply (e.g. orchestrator)
   ```
4. Set model profiles in `configs/models.yaml` (replace any `TBD` values).
5. Validate:
   ```bash
   scripts/07-validate-harness.sh
   ```
6. If the template includes the orchestrator, also run:
   ```bash
   python3 -m unittest discover scripts/orchestrator/tests
   ```
7. Start work at `stages/01-task-definition/` or via `/plan`.

### For maintainers (publish or refresh the template)

1. Run the release checklist:
   ```bash
   scripts/08-prepare-template-release.sh
   ```
2. On GitHub → **Settings** → **General** → enable **Template repository**.
3. Tag a release (e.g. `v1.0.0`) with notes pointing to this file and `skills/new-project.md`.
4. Confirm bootstrap still works (the release script dry-runs this automatically):
   ```bash
   scripts/01-create-project.sh --with-orchestrator
   ```

**What ships in a template repo:** full folder tree (`agents/`, `skills/`, `prompts/`, `configs/`, `evals/`, `stages/`, `plans/`, `scripts/`, etc.). Optional orchestrator is included when using `--with-orchestrator` during local bootstrap; the canonical template repo should include orchestrator files if you advertise Phase 01–04 support.

---

## Path B — Local bootstrap (no GitHub template)

Best for: scaffolding into an existing machine, a non-GitHub VCS, or a path outside your home directory layout.

### From this repo (source of truth)

```bash
# Interactive — prompts for destination path
scripts/01-create-project.sh

# Include Native Orchestrator (Python stdlib CLI + tests)
scripts/01-create-project.sh --with-orchestrator

# Non-interactive
HARNESS_PROJECT_PATH=~/projects/my-app-harness HARNESS_OVERWRITE=1 \
  scripts/01-create-project.sh --with-orchestrator
```

The generator copies canonical harness files, renames the `CLAUDE.md` title to the project folder name, and runs `scripts/07-validate-harness.sh`.

### After bootstrap

1. `cp _config/project-notes.TEMPLATE.md _config/project-notes.md` and fill in project-specific commands.
2. Configure `configs/models.yaml`.
3. Delete template-only artifacts you do not need (see [Trimming optional features](#trimming-optional-features)).
4. Initialize git in the new folder if it is a standalone project.

Skill reference: `skills/new-project.md`.

---

## Path C — Monorepo subfolder (attach to an existing app)

Best for: keeping application code and harness context in one repository without replacing the app root.

### Layout

```text
my-app/
├── src/                    # your application
├── tests/
└── harness/                # or .harness/, docs/agent-harness/
    ├── CLAUDE.md
    ├── FRAMEWORK.md
    ├── agents/
    ├── skills/
    ├── configs/
    ├── evals/
    ├── stages/
    ├── scripts/
    └── _config/project-notes.md
```

### Steps (recommended: app-aware installer)

The ergonomic path is `scripts/new-project.sh`, which wraps the subfolder
bootstrap below **and** wires the harness to the app: it re-titles `CLAUDE.md`
to the app name, generates `_config/project-notes.md` (Name, Repo, detected
verify command, `App root: ..`), seeds an initial task from a one-line goal, and
hands off to `/plan` to start development.

```bash
# Prompts for the project goal, installs into ./my-app/harness/
scripts/new-project.sh ./my-app --with-orchestrator
# (a root symlink is provided too: ./new-project.sh ./my-app --with-orchestrator)

# Non-interactive
HARNESS_TARGET_REPO=./my-app \
HARNESS_PROJECT_GOAL="Add a /health endpoint" HARNESS_OVERWRITE=1 \
  scripts/new-project.sh --with-orchestrator
```

Then follow `skills/new-project.md` to auto-continue into `/plan` (it reads the
`.harness-handoff` marker the installer wrote). Point AI assistants at
`harness/CLAUDE.md` (Cursor rule, `AGENTS.md` symlink, or workspace multi-root),
and keep portable skills generic — app-specific paths live only in
`project-notes.md` (see `FRAMEWORK.md` → Deployment overlay).

### Steps (manual subfolder bootstrap)

If you only need the raw folder tree without the app wiring or `/plan` handoff:

1. Bootstrap into a subfolder:
   ```bash
   HARNESS_PROJECT_PATH=./my-app/harness scripts/01-create-project.sh --with-orchestrator
   ```
2. In `_config/project-notes.md`, set **Verify green** to your app’s test commands *and* harness validation:
   ```bash
   scripts/07-validate-harness.sh
   npm test   # example — your app
   ```
3. Point AI assistants at `harness/CLAUDE.md`.
4. Keep portable skills generic; put app-specific paths only in `project-notes.md`.

### CI suggestion

Run harness validation separately from app tests so structural drift is caught early:

```bash
PROJECT_ROOT=./harness ./harness/scripts/07-validate-harness.sh
```

---

## Path D — PyPI package (orchestrator only, optional)

Best for: reusing **only** the stdlib Python coordinator in non-harness repos. **Not recommended** as the primary distribution model — most harness value lives in markdown artifacts, not importable Python.

| Include in PyPI | Keep as template copy |
|-----------------|----------------------|
| `scripts/orchestrator/` | `agents/`, `skills/`, `prompts/`, `evals/`, `stages/` |
| `scripts/orchestrate.py` | `configs/*.yaml` (project-specific) |
| YAML subset parser, sequencer, runlog | Lifecycle contracts and rubrics |

If you pursue this path:

1. Extract `scripts/orchestrator/` into a standalone package with `pyproject.toml`.
2. Accept `PROJECT_ROOT` or `--root` so configs resolve against the consumer repo.
3. Document that consumers must still supply `configs/routing.yaml`, agent contracts, and telemetry schema — or ship those as optional package data.
4. Publish separately from the template; version the template and PyPI package on different cadences.

The harness maintainers do **not** ship PyPI today. Use Path A or B unless you have a concrete reuse case for the orchestrator alone.

---

## Trimming optional features

Bootstrapped projects may omit subsystems they do not use (`_config/PORTABILITY-VERIFICATION.md`):

| Remove if unused | Paths |
|------------------|-------|
| Native Orchestrator | `scripts/orchestrate.py`, `scripts/orchestrator/`, `plans/native-orchestrator/`, `evals/cases/orchestrator/`, orchestrator section in `project-notes.md` |
| GitNexus indexing | `package.json`, `.claude/skills/gitnexus/` |
| Dogfood / meta plans | `plans/improve-*`, `evals/results/*` from upstream template |

After trimming, re-run `scripts/07-validate-harness.sh`. Orchestrator-specific rubrics and eval cases can remain; they only matter if you run orchestrator evals.

---

## Versioning and compatibility

- **Template releases:** tag semver on the harness repo (`v1.0.0`). Release notes should mention validator check counts and whether orchestrator Phase 01–04 is included.
- **No install step:** Python 3.9+ stdlib only for orchestrator; no `pip install` for core harness.
- **Breaking changes:** renaming agents, skills, or config keys requires updating `configs/agents.yaml`, `configs/routing.yaml`, and cross-references — run the validator after merges.

---

## Quick comparison

| Goal | Path | Install step |
|------|------|--------------|
| New repo from GitHub | A — Template | None |
| Local folder / script | B — Bootstrap | None |
| Harness beside app code | C — Monorepo subfolder | None |
| Python coordinator only | D — PyPI (DIY) | `pip install` (custom) |

---

## Related docs

- `README.md` — what the harness is
- `TUTORIAL.md` — step-by-step: new project, existing project, first lifecycle
- `FRAMEWORK.md` — concepts and deployment overlay
- `skills/new-project.md` — agent procedure for bootstrap
- `_config/PORTABILITY-VERIFICATION.md` — portability proof
- `scripts/08-prepare-template-release.sh` — maintainer checklist before tag/release
