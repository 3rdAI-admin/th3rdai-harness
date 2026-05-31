---
description: Install the harness into an existing app/repo and hand off to /plan
---

# New Project — Install the Harness and Start Development

This is the **first step** for using the harness against a project. It installs
the harness into a **segmented subfolder** of an existing app/repo (default
`harness/`), wires it to orchestrate that app, seeds an initial task from a
one-line goal, and then **hands off to the `/plan` process** to begin
development.

There are two modes:

- **Install into an existing app/repo** (primary) — `scripts/new-project.sh`.
  The harness lives beside the app code and develops it from `..`.
- **Scaffold a standalone harness** (folder of its own) — `scripts/01-create-project.sh`.

## Harness References

- Primary installer: `scripts/01-create-project.sh` wrapped by `scripts/new-project.sh`
- Standalone scaffolder: `scripts/01-create-project.sh` (add `--with-orchestrator`)
- PLAN process: `skills/plan/SKILL.md` → `skills/plan/planner.md`
- Distribution paths: `DISTRIBUTION.md` (GitHub template, monorepo subfolder, release checklist)
- Tutorial: `TUTORIAL.md` (new project, existing project, first lifecycle)
- Validation: `scripts/07-validate-harness.sh`
- Framework: `FRAMEWORK.md`
- Routing: `CONTEXT.md`
- Deployment overlay: generated `_config/project-notes.md` (from `_config/project-notes.TEMPLATE.md`)

## Input: $ARGUMENTS

- Path to the target app/repo (e.g. `~/projects/my-app` or `.`). Defaults to the
  current directory. The harness installs into `<target>/harness/`.

## Process

### 1. Install into the app/repo

Use the app-aware installer. It prompts for a one-line project goal, then lays
down the harness and wires it to the app:

```bash
scripts/new-project.sh <target-app-path>
# include the Native Orchestrator CLI:
scripts/new-project.sh <target-app-path> --with-orchestrator
# a root symlink is also provided, so from the harness root you can run:
./new-project.sh <target-app-path>
```

The installer is current-directory independent (it locates its delegate via its
own path), so it can be called from anywhere; only `<target-app-path>` matters.

Non-interactive:

```bash
HARNESS_TARGET_REPO=~/projects/my-app \
HARNESS_PROJECT_GOAL="Add a /health endpoint that returns build version" \
HARNESS_OVERWRITE=1 \
  scripts/new-project.sh --with-orchestrator
```

Environment overrides: `HARNESS_TARGET_REPO`, `HARNESS_SUBDIR` (default
`harness`), `HARNESS_PROJECT_GOAL`, `HARNESS_OVERWRITE=1`.

The installer delegates the folder-tree copy to `scripts/01-create-project.sh`
(single source of truth), then:

- Re-titles `harness/CLAUDE.md` to the **app name** (not "harness").
- Generates `harness/_config/project-notes.md` with the app **Name**, **Repo**,
  a stack-detected verify command, and **App root: `..`** — the anchor that
  tells harness skills the app under development lives one level up.
- Seeds `harness/stages/01-task-definition/INITIAL.md` from the goal (the seed
  points `/plan` at the app `..` and at `project-notes.md`).
- Writes the handoff marker `harness/.harness-handoff`.

> Standalone alternative: to scaffold a harness as its own root folder instead,
> run `scripts/01-create-project.sh` (see `DISTRIBUTION.md` Path A/B).

### 2. Segmentation and orchestration model

```text
my-app/                      # the application (untouched by install)
├── src/ … tests/ …          # app code
└── harness/                 # the harness — segmented, but orchestrates ..
    ├── CLAUDE.md            # titled with the app name
    ├── stages/01-task-definition/INITIAL.md   # seeded task
    ├── _config/project-notes.md               # Name, Repo, App root: ..
    └── .harness-handoff                        # → plan stages/01-task-definition/INITIAL.md
```

All development work targets the app at `..`. App-specific paths and verify
commands live in `project-notes.md`, keeping the portable skills generic
(`FRAMEWORK.md` → Deployment overlay). Point AI assistants at `harness/CLAUDE.md`.

### 3. Hand off to the PLAN process (auto-continue)

A shell script cannot invoke `/plan` itself, so this skill completes the
handoff. **After the installer finishes, operating from the harness root
(`harness/`):**

1. Check for the handoff marker `.harness-handoff`.
2. If present, read the next action (`plan <seed-path>`) and **immediately run
   the `/plan` process** on that seed:

   ```text
   /plan stages/01-task-definition/INITIAL.md
   ```

   (Follow `skills/plan/SKILL.md` → `skills/plan/planner.md`; the planner reads
   `_config/project-notes.md` and explores the app at `..`.)
3. **Clear the marker** (delete `.harness-handoff`) once `/plan` has started, so
   it is not re-triggered. Re-running the installer regenerates it.
4. If running as a human (not an agent), the installer already printed the exact
   `/plan` command — run it yourself.

### 4. Validation

The installer runs `scripts/07-validate-harness.sh` against the subfolder and
prints the `Passed / Warnings / Failed` summary. To re-run:

```bash
PROJECT_ROOT=<target>/harness <target>/harness/scripts/07-validate-harness.sh
```

Capture the actual summary from script output (do not hardcode counts).

### 5. Output

```text
HARNESS INSTALLED: <target>/harness  (orchestrating <app-name>)

Goal:       <one-line goal>
Validation: Passed: N  ·  Warnings: N  ·  Failed: 0

Next: /plan stages/01-task-definition/INITIAL.md  (auto-continued by this skill)
```

## Example Usage

```text
/new-project ~/projects/my-app
/new-project .
/new-project ~/projects/my-app --with-orchestrator
```

## Error Handling

- **Target does not exist:** the installer exits; provide a valid app path.
- **`harness/` already exists:** the installer asks to overwrite (or set
  `HARNESS_OVERWRITE=1`); decline and choose a different `HARNESS_SUBDIR`.
- **Empty goal:** the `/plan` handoff needs a goal; the installer exits — re-run
  with a goal.
- **Not a git repo / no remote:** the **Repo** field falls back to the target
  path; install proceeds (git is informational).
- **Validation fails:** report failed checks and fix the installed structure
  before running `/plan`.

## Success Criteria

- Harness installed into the app's `harness/` subfolder; app code untouched.
- `CLAUDE.md` titled with the app name; `project-notes.md` records the app and
  `App root: ..`.
- Seeded `INITIAL.md` and `.harness-handoff` present.
- Validation passes.
- `/plan` started from the seeded task (marker cleared).
