---
description: >-
  Audit skills for scriptable steps, propose script-optimized migrations, and mine
  conversation history for new skills to create. Use when the user asks to
  script-optimize skills, find programmatic skill steps, or invent new skills from
  chat history.
name: skill-script-audit
---

# Skill Script Audit — Scriptability + New-Skill Discovery

Loaded by `/skill-script-audit` via `skills/skill-script-audit/SKILL.md`.

> **Goal:** Find where skills are doing **deterministic, repeatable work that belongs
> in scripts**, explain how to migrate those steps, and propose **additional skills**
> justified by real conversation history — without implementing unless asked.

## Harness References

- Skill manifests: `skills/*/SKILL.md` (when this repo is vendored as `harness/`, also
  check `harness/skills/`), plus host overlays listed in `_config/project-notes.md`
  (examples, persona packs, forge/extra skill dirs — if present)
- Framework: `FRAMEWORK.md`, `CONTEXT.md`
- Related skills: `skills/revise/`, `skills/research/`, `skills/plan/`
- Deployment overlay (optional): `_config/project-notes.md`

## Input: $ARGUMENTS

Host-interpolated arguments (when the runtime supports them): {input}

- Optional scope: `skills` | `examples` | `forge` | a skill name | a path.
  Default: all discovered skill roots for this project.
- Optional flags in free text: `history-only`, `scripts-only`, `write-plan`
  (`write-plan` drafts `plans/skill-script-audit-<date>.md` — still no code).

Only one of `$ARGUMENTS` / a host-specific input line will be populated; treat whichever
is filled as the arguments.

## Process

### 1. Inventory skills (read-only)

Discover skill folders with a manifest (`SKILL.md` / `skill.md`):

| Root | Typical contents |
|------|------------------|
| `skills/` (or `harness/skills/` when vendored) | Lifecycle / harness skills |
| `examples/skills/` | Demo / product examples (if present) |
| Host overlay dirs from `_config/project-notes.md` | Persona packs, forge, extras |

For each skill record: name, path, description, optional frontmatter (`persona:` /
`model:` / `context:` if any), whether it uses `prompts/` vs a procedure file, and
approximate size (lines).

Skip `_Archived/`, `node_modules`, and binary skill/plugin archives unless the user
asks to unpack them (prefer already-converted plain-text skill folders).

### 2. Score steps for scriptability

Read each skill's procedure / prompts. Split into **steps**. Tag each step:

| Tag | Meaning | Prefer |
|-----|---------|--------|
| `SCRIPT` | Deterministic, same I/O every time, no judgment | Shell / Python script under `scripts/` or skill-local `scripts/` |
| `TOOL` | Needs host tools but still mechanical (list files, run tests, format) | Thin script wrapping existing CLIs |
| `LLM` | Requires language judgment, drafting, triage, design | Keep in skill prompts |
| `GATE` | Human approval, merge, spend/autonomy policy | Keep in skill; never automate away |

**SCRIPT heuristics (positive signals):**

- Fixed file transforms (unzip → copy → rename; frontmatter rewrite; TOC generation)
- Inventory / grep / list / diff / checksum / format / lint invocations with stable flags
- Template fill from structured JSON/YAML (no prose invention)
- "Run X then parse stdout into a table" with a stable schema
- Idempotent setup (mkdir, copy assets, write stub if missing)

**LLM heuristics (keep in skill):**

- "Infer", "judge", "draft in voice", "decide priority", "review quality"
- Open-ended research synthesis without a fixed schema
- Persona / brand-brain client-facing copy

Emit only **actionable** SCRIPT/TOOL candidates (skip trivial one-liners already fine
as a single shell example inside the skill).

### 3. Migration recipe per candidate

For each SCRIPT/TOOL candidate, write a migration block:

```markdown
### <skill-name> → <step short title>
- **Today:** (quote or paraphrase the skill step; path + line/section)
- **Why script:** (determinism / speed / token cost / fewer failure modes)
- **Proposed script:** `scripts/<name>.sh` or `scripts/<name>.py` (stdlib-first)
- **CLI sketch:** args, exit codes, stdout schema (JSON preferred for agent consumption)
- **Skill after migration:** keep LLM/GATE steps; replace SCRIPT step with
  "Run `…`; then interpret results…"
- **Validation:** how to prove parity (fixture in → expected out)
- **Risk:** LOW/MEDIUM/HIGH — note if call-graph / impact analysis is needed when wiring
```

**Migration principles:**

1. Skills **orchestrate**; scripts **compute**.
2. Scripts must be dependency-light (prefer Python stdlib / bash already used by harness).
3. Scripts print structured output agents can trust; skills narrate and decide.
4. Do not move GATE or persona voice into scripts.
5. Prefer one script per stable pipeline; avoid micro-scripts for single `mkdir`.

### 4. Mine conversation history for new skills

Search **evidence**, do not invent. Sources (use what exists for this machine/repo):

| Source | Path / how |
|--------|------------|
| IDE agent transcripts | Cursor/Claude local transcript dirs for this workspace (if present) |
| Session / memory notes | Host memory or session folders listed in project notes |
| Handoff / ops | `HANDOFF.md`, `handoff/*.md`, ops/troubleshoot docs (if present) |
| Plans / efforts | `plans/`, repo-root `*PLAN*.md`, `*UPDATE*.md` |
| Prior skill PRs | `git log --oneline -- skills` |

Look for **repeated workflows** the user or agents re-derived in chat (same steps ≥2
times, or one high-value workflow explicitly requested as reusable).

For each proposed new skill:

```markdown
### Proposed: <skill-name>
- **Trigger phrases:** …
- **Job:** one sentence
- **Evidence:** transcript/session/handoff cite (path + short quote/paraphrase)
- **Overlap check:** existing skill it might extend instead of duplicating
- **Priority:** P0/P1/P2
- **First slice:** minimal SKILL.md + procedure outline (no full implementation yet)
```

Overlap rule: if `revise`, `plan`, `research`, or an existing domain skill already
covers ≥70% of the job, recommend **extending** that skill rather than adding a new one.

### 5. Write the report

Default path: `runs/skill-script-audit-<YYYYMMDD>-<HHMM>.md`
(or print in-chat if the host cannot write). When this harness is vendored under
`harness/`, prefer `harness/runs/…` if that is the project's convention.

Required sections:

1. **Scope** — roots audited, filters applied
2. **Inventory** — table of skills reviewed
3. **Scriptability findings** — migration recipes (Section 3)
4. **New skill backlog** — history-grounded proposals (Section 4)
5. **Recommended next actions** — ordered; note `/plan` only if user wants build-out
6. **Out of scope / deferred** — anything skipped and why

If arguments include `write-plan`, also draft
`plans/skill-script-audit-<YYYYMMDD>.md` using the planner template sections
(Goal, Scope, Steps, Validation, Files, Risks) — still **no code changes**.

## Validation Criteria

- [ ] Every SCRIPT/TOOL finding cites a real skill path and step
- [ ] Every new-skill proposal cites history/handoff/plan evidence (or is explicitly
      marked `hypothesis — unconfirmed`)
- [ ] No silent implementation; report is the deliverable unless user opts in
- [ ] Overlap check performed against the local `skills/` inventory
- [ ] Report path recorded (or full report inlined if write unavailable)

## Anti-patterns

- Rewriting all skills into scripts (LLM judgment must stay in skills)
- Proposing skills that duplicate `/plan`, `/research`, `/build` under new names
- "New skill" ideas with no transcript/session/handoff evidence
- Implementing migrations in the same turn as the audit without approval
- Treating binary skill/plugin zips as runtime skills when a plain-text copy exists

## Autonomy Mode Recommendation

```bash
python3 scripts/orchestrate.py route iteration --execute --adapter cli --autonomy ask
```

Prefer **ask** / **cautious**: this skill is advisory; implementation is a separate,
gated follow-on.

## Success

The user receives a concrete Scriptability Report + New Skill Backlog they can accept,
reject, or feed to `/plan` — with zero unsolicited repo mutations.
