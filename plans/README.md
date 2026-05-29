# Plans

Home for implementation-ready plans produced by the Planner Agent (`/plan`).

This is a native harness convention — it depends on no external tooling. Plans are plain-text, version-controllable, and driven by an agent or human following the lifecycle in `FRAMEWORK.md`.

## Layouts

Choose the smallest layout that fits the work.

### Single plan

For a self-contained change, write one file:

```text
plans/<plan-name>.md
```

Use the plan template from `skills/plan/planner.md`.

### Multi-phase effort

For complex development that spans multiple dependent plans, group them under an effort folder with a tracker:

```text
plans/<effort-name>/
  EFFORT.md          # goal, phases, dependency order, status tracker
  01-<phase>.md      # phase plan (uses the planner template)
  02-<phase>.md
  ...
```

`EFFORT.md` is the source of truth for sequencing and status. See `plans/_template-effort/EFFORT.md` for the structure.

## Conventions

- Name plans and phases with a short, lowercase, hyphenated slug.
- Number phases when order matters (`01-`, `02-`, ...).
- Record dependencies explicitly in `EFFORT.md` — the harness has no scheduler, so the dependency order is what an agent/human follows.
- Update status in `EFFORT.md` as phases move: `todo → doing → review → done`.
- When a plan is executed, link its run record(s) in `runs/` and any eval results in `evals/results/`.
- Add notable plans/efforts to `plans/INDEX.md`.

## Lifecycle Fit

```text
/research → /plan → /plan-reviewer → /build → /validate + /eval → /gitcommit
```

Plans are created in Stage 01 (Task Definition) and consumed by the Builder Agent in later stages.
