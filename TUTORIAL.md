# Harness Tutorial

Walk through using the AI Agent Development Harness in two common setups:

1. **New project** — a fresh repo whose primary job is agent/model work (or a greenfield app you build *with* the harness).
2. **Existing project** — an app that already has code; you attach the harness beside it.

This tutorial assumes you work with a capable AI assistant (Cursor, Claude Code, etc.) that reads `CLAUDE.md` and follows skills. The harness does not run agents autonomously — **you or your assistant drive the lifecycle**, guided by contracts in plain text.

**Related docs:** `README.md` (overview) · `DISTRIBUTION.md` (how to copy or publish the template) · `FRAMEWORK.md` (concepts)

---

## Before you start

| Requirement | Notes |
|-------------|--------|
| **Python 3.9+** | Only needed for validation scripts and the optional orchestrator CLI |
| **Git** | Recommended for both setups |
| **AI assistant** | Should load `CLAUDE.md` (or point rules at `harness/CLAUDE.md` in monorepos) |
| **No pip/npm install for the harness** | Core harness is plain text + bash; orchestrator is stdlib-only |

**Core idea:** The harness separates *who* (agents), *how* (skills), *what to say* (prompts), *which model* (configs), and *how to measure* (evals). You move work through seven lifecycle stages; each stage has a contract in `stages/*/CONTEXT.md`.

```text
Task Definition → Agent Design → Prompt Design → Tool Integration
      → Evaluation → Iteration → Release
```

---

## Part I — New project

Use this when the harness **is** the project (agent development, prompt engineering, eval workflows) or when you are starting a new app and want the harness from day one.

### Step 1: Create the project

Pick one:

**GitHub template (team / open source)**

1. On GitHub: **Use this template** → create a new repository.
2. Clone locally: `git clone git@github.com:you/my-harness-project.git`

**Local bootstrap (from a copy of this repo)**

```bash
# From the harness template repo:
scripts/01-create-project.sh --with-orchestrator

# Or non-interactive:
HARNESS_PROJECT_PATH=~/projects/invoice-review-agent HARNESS_OVERWRITE=1 \
  scripts/01-create-project.sh --with-orchestrator
```

`--with-orchestrator` copies the optional Python coordinator (`scripts/orchestrate.py`). Skip it if you only want the markdown framework.

### Step 2: Validate structure

```bash
cd ~/projects/invoice-review-agent   # your project root
scripts/07-validate-harness.sh
```

Expect **Passed** with **Failed: 0**. Fix any missing files before continuing.

If you included the orchestrator:

```bash
python3 -m unittest discover scripts/orchestrator/tests -q
```

### Step 3: Configure project identity

```bash
cp _config/project-notes.TEMPLATE.md _config/project-notes.md
```

Edit `_config/project-notes.md`:

- Set **Project name**, repo URL, and tracking (issue tracker / Archon ID if you use one).
- Fill **Verify green** with commands that apply (harness validator at minimum).
- Delete sections you do not need (e.g. orchestrator if you skipped it).

Set models in `configs/models.yaml` for your environment (provider + model IDs). The template ships with Claude-family defaults — swap to what you actually use.

### Step 4: Point your AI assistant at the harness

Open the project root in Cursor (or your IDE). The assistant should read:

1. `CLAUDE.md` — operating rules
2. `CONTEXT.md` — which stage to use
3. `_config/project-notes.md` — your local commands and shortcuts

Optional: add a Cursor rule that says “Start with `CLAUDE.md` and `CONTEXT.md`.”

### Step 5: Initialize git (if not from GitHub template)

```bash
git init
git add .
git commit -m "Initial harness scaffold"
```

### New-project checklist

- [ ] Validator passes (`scripts/07-validate-harness.sh`)
- [ ] `_config/project-notes.md` filled in (not the TEMPLATE)
- [ ] `configs/models.yaml` has real provider/model values
- [ ] Assistant loads `CLAUDE.md`
- [ ] Ready to start at Stage 01 (below)

---

## Part II — Existing project

Use this when you already have an application (e.g. `src/`, `package.json`, `pyproject.toml`) and want harness context **without** replacing your repo root.

### Example layout

```text
taskflow/                      # your existing app
├── src/
├── tests/
├── package.json
└── harness/                   # harness subfolder
    ├── CLAUDE.md
    ├── FRAMEWORK.md
    ├── CONTEXT.md
    ├── agents/
    ├── skills/
    ├── configs/
    ├── evals/
    ├── stages/
    ├── scripts/
    └── _config/project-notes.md
```

### Step 1: Install with the app-aware installer

From your machine (with access to the harness template), run `new-project.sh`
against your app. It installs into `taskflow/harness/`, **and** wires the
harness to the app: re-titles `CLAUDE.md` to the app name, pre-fills
`_config/project-notes.md` (Name, Repo, detected verify command, `App root:
..`), seeds an initial task from a one-line goal, and writes a `/plan` handoff
marker.

```bash
/path/to/th3rdai-harness/scripts/new-project.sh ~/projects/taskflow --with-orchestrator
# prompts for the project goal, then installs + wires + seeds /plan
```

Non-interactive:

```bash
HARNESS_TARGET_REPO=~/projects/taskflow \
HARNESS_PROJECT_GOAL="Add a /health endpoint" HARNESS_OVERWRITE=1 \
  /path/to/th3rdai-harness/scripts/new-project.sh --with-orchestrator
```

Because the installer pre-fills `project-notes.md` and seeds the task, Steps 2–3
below become a quick review rather than from-scratch setup. (To lay down only
the raw tree without wiring, use `scripts/01-create-project.sh` with
`HARNESS_PROJECT_PATH=./harness` instead.)

### Step 2: Wire the assistant to the subfolder

Tell your AI assistant where the harness lives:

- **Cursor:** workspace includes repo root; add a rule: “For agent harness work, read `harness/CLAUDE.md` and `harness/CONTEXT.md`.”
- **Monorepo:** you can symlink `AGENTS.md` → `harness/CLAUDE.md` at repo root if your tools expect `AGENTS.md` there.

Do **not** duplicate app-specific paths inside portable skills. Put them only in `harness/_config/project-notes.md`.

### Step 3: Review the generated project-notes

`new-project.sh` already generated `harness/_config/project-notes.md` with the
app **Name**, **Repo**, **App root: `..`**, and a detected verify command.
Review and extend it — add lint commands, research shortcuts, and resume
pointers:

```markdown
## Project

**Name:** TaskFlow
**Repo:** https://github.com/you/taskflow

## Verify green (this project)

scripts/07-validate-harness.sh          # run from harness/
npm test                                 # app tests from repo root
npm run lint

## Research shortcuts

- **Application code:** `src/`
- **API routes:** `src/routes/`
- **Harness agents:** `harness/agents/`
```

Adjust paths to your stack. The harness validator runs with:

```bash
PROJECT_ROOT=./harness ./harness/scripts/07-validate-harness.sh
```

### Step 4: Commit the harness folder

```bash
git add harness/
git commit -m "Add agent development harness under harness/"
```

### Step 5: Optional CI

Add a job that only validates harness structure:

```bash
PROJECT_ROOT=harness harness/scripts/07-validate-harness.sh
```

Keep app tests separate — the harness checks contracts and cross-references, not your product logic.

### Existing-project checklist

- [ ] `harness/` validates independently
- [ ] `project-notes.md` documents app paths and test commands
- [ ] Assistant knows to use `harness/` for lifecycle work
- [ ] Portable skills unchanged; app specifics only in project-notes
- [ ] Development started via the seeded task: `/plan stages/01-task-definition/INITIAL.md` (see `skills/new-project.md`)

---

## Part III — Your first lifecycle (worked example)

This section applies to **both** setups. Paths assume project root is the harness root; if you use a monorepo, prefix with `harness/`.

**Scenario (new project):** Build an **invoice review agent** — an agent contract + prompt that flags PCI-related fields in uploaded invoices.

**Scenario (existing project):** Same flow, but research steps also read `src/` via project-notes shortcuts.

### Stage 01 — Task definition

**Goal:** Agree on scope before writing agents or prompts.

1. Open `stages/01-task-definition/CONTEXT.md` (or ask your assistant to follow it).
2. Create a task brief:

```bash
mkdir -p stages/01-task-definition/output
```

3. Ask your assistant:

```text
Follow stages/01-task-definition/CONTEXT.md. I want an invoice review agent
that flags PCI-related fields in PDF invoices. Write output/task-definition.md
with success criteria, scope, and open questions.
```

4. **Checkpoint:** Read `stages/01-task-definition/output/task-definition.md`. Confirm scope before Stage 02.

**Skill alternative:** `/research` then `/plan` on your brief — the planner skill (`skills/plan/planner.md`) produces `plans/<name>.md` if you prefer a plan-first workflow.

### Stage 02 — Agent design

**Goal:** Define role, permissions, inputs, outputs, handoffs.

1. Read `agents/researcher.agent.md` and `agents/reviewer.agent.md` as examples.
2. Ask your assistant:

```text
Follow stages/02-agent-design/CONTEXT.md. Create agents/invoice-reviewer.agent.md
with explicit tool permissions (read files, no network unless approved).
Register the agent in configs/agents.yaml.
```

3. Verify routing if this agent joins a route — edit `configs/routing.yaml` only when you orchestrate multi-step flows.

4. Run validator after config changes:

```bash
scripts/07-validate-harness.sh
```

### Stage 03 — Prompt design

**Goal:** Version the instruction template the agent uses.

1. Create `prompts/invoice-reviewer/v1.md`.
2. Register it in `prompts/registry.md`.
3. Ask for a reviewer pass:

```text
Follow stages/03-prompt-design/CONTEXT.md. Review prompts/invoice-reviewer/v1.md
against agents/invoice-reviewer.agent.md. Note gaps in output/prompt-changelog.md.
```

### Stage 04 — Tool integration

**Goal:** Document runtime behavior, scripts, and safety boundaries.

For a harness-only agent, this may mean:

- Updating `configs/tools.yaml` with allowed/disallowed commands
- Adding a skill under `skills/` if there is a repeatable procedure
- Documenting any app integration in `_config/project-notes.md` (existing project)

Ask:

```text
Follow stages/04-tool-integration/CONTEXT.md. Document tool policy for the
invoice reviewer in configs/tools.yaml and add a skill stub if needed.
```

### Stage 05 — Evaluation

**Goal:** Measure quality with a rubric before you “ship” the agent.

1. Pick or create an eval case: `evals/cases/<category>/<case>.md`
2. Pick a rubric: e.g. `evals/rubrics/agent-output-quality.md`
3. Run the eval skill:

```text
/eval agents/invoice-reviewer.agent.md using evals/cases/... and
evals/rubrics/agent-output-quality.md
```

4. Save results under `evals/results/YYYYMMDD-<slug>.md`.

**Orchestrator shortcut (if installed):**

```bash
python3 scripts/orchestrate.py eval evals/cases/planning/basic-feature-plan.md
```

This scaffolds a PENDING result + run record; you still score with the evaluator agent.

### Stage 06 — Iteration

**Goal:** Fix gaps found in evals.

```text
Follow stages/06-iteration/CONTEXT.md. Address failures in
evals/results/YYYYMMDD-invoice-reviewer.md. Update prompt v1 or plan v2.
Re-run /eval.
```

Repeat until rubric scores meet your bar.

### Stage 07 — Release

**Goal:** Document what changed and validate before commit.

1. Follow `stages/07-release/CONTEXT.md`.
2. Run verify-green commands from `_config/project-notes.md`.
3. Ask for release notes:

```text
Follow stages/07-release/CONTEXT.md. Write output/release-notes.md summarizing
the invoice reviewer agent, prompt v1, eval score, and validation commands run.
```

4. Commit only with explicit approval (`skills/commit/gitcommit.md`).

---

## Part IV — Working with skills and agents

Skills are procedures in `skills/`. Agents are role contracts in `agents/`. Your assistant loads a skill when you invoke a command like `/plan` or when routing selects an agent.

| You want to… | Start with | Agent |
|--------------|------------|--------|
| Clarify requirements | `/research` or Stage 01 | Researcher |
| Write a plan | `/plan` | Planner |
| Review a plan | `/plan-reviewer` | Reviewer |
| Implement harness/app changes | `/build` | Builder |
| Run structural checks | `/validate` | Builder / Reviewer |
| Score an artifact | `/eval` | Evaluator |
| Start a dev server or validator | `/run` | Builder |
| Safe git commit | `/gitcommit` | Reviewer |
| Scaffold new harness repo | `/new-project` | Builder |

**Routing:** `CONTEXT.md` maps user intent → stage folder. `configs/routing.yaml` maps route names → ordered agents (used by the orchestrator).

**Deployment overlay:** Before any skill runs optional tooling, it should read `_config/project-notes.md` if present — that is where **your** test commands, app paths, and orchestrator notes live.

---

## Part V — Optional orchestrator CLI

The orchestrator **coordinates**; it does not replace your AI assistant. It sequences stages, assembles context bundles, and writes run records.

```bash
# Dry-run: show steps and context bundles for a lifecycle route
python3 scripts/orchestrate.py route task_definition

# Scaffold an eval run record
python3 scripts/orchestrate.py eval evals/cases/planning/basic-feature-plan.md

# Opt-in execution (approval-gated; requires configs/execution.yaml)
python3 scripts/orchestrate.py route iteration --execute --adapter cli --max-steps 1
```

Routes: `task_definition`, `agent_design`, `prompt_design`, `tool_integration`, `evaluation`, `iteration`, `release`.

**When to use it:** repeatable run logging, eval scaffolding, or step-by-step execute experiments. **When to skip it:** pure manual/agent-driven flow — the harness works without it (`_config/PORTABILITY-VERIFICATION.md`).

---

## Part VI — Day-two operations

### Adding a second feature or agent

1. New task definition under `stages/01-task-definition/output/` (or new `plans/<feature>.md`).
2. Reuse or extend agents; add prompt versions (`v2`, `v3`) rather than overwriting without changelog.
3. Add eval cases under `evals/cases/`.
4. Record runs under `runs/` per `telemetry/run-log-schema.md`.

### Keeping the harness healthy

```bash
scripts/07-validate-harness.sh
```

Run after changing `configs/agents.yaml`, `configs/routing.yaml`, or `prompts/registry.md`.

### Trimming features you do not use

See `DISTRIBUTION.md` → *Trimming optional features*. Remove orchestrator paths if you never use the CLI; delete meta `plans/` from upstream if irrelevant.

---

## Quick reference

| Task | Command / location |
|------|---------------------|
| New standalone project | `scripts/01-create-project.sh --with-orchestrator` |
| Attach to existing app | Bootstrap into `./harness/` — Part II |
| Validate harness | `scripts/07-validate-harness.sh` |
| Where to start work | `stages/01-task-definition/` or `/plan` |
| Local commands & app paths | `_config/project-notes.md` |
| Model choices | `configs/models.yaml` |
| Tool safety | `configs/tools.yaml` |
| Publish template | `DISTRIBUTION.md` + `scripts/08-prepare-template-release.sh` |

---

## Troubleshooting

| Problem | Likely fix |
|---------|------------|
| Validator fails: `plans/ is missing` | Re-run bootstrap from an updated template, or `mkdir plans && cp …/plans/README.md plans/` |
| Validator fails: agent/routing mismatch | Every agent in `configs/routing.yaml` needs `agents/<name>.agent.md` |
| Assistant ignores harness | Point rules at `CLAUDE.md` (or `harness/CLAUDE.md`); mention `CONTEXT.md` in first message |
| Skills reference wrong paths (monorepo) | Put app paths in `project-notes.md`; invoke skills with harness-relative paths |
| Orchestrator import errors | Run from repo root: `python3 scripts/orchestrate.py`; use `from scripts.orchestrator import …` in tests |
| `models.yaml` warnings | Replace `TBD` provider/model with real values |

---

## Next steps

1. Complete Part I or Part II for your situation.
2. Run Part III with a **small real task** (one agent or one prompt revision).
3. Read `FRAMEWORK.md` for the full conceptual model.
4. When ready to share the template, follow `DISTRIBUTION.md`.

For meta-development on the harness itself, see `HANDOFF.md` and `VERSION3.md`.
