---
description: Re-organize a repo to professional structure and archive clutter without breaking behavior
name: code-cleanup
---

# Code Cleanup — Re-organize Without Breaking Anything

Loaded by `/code-cleanup` via `skills/code-cleanup/SKILL.md`.

> **Goal:** Re-organize the codebase to professional, industry-standard structure and remove
> clutter — **without changing or breaking any behavior**. Obsolete files are *archived to
> `archive/`*, not deleted, so the prior state can always be restored.

This procedure is intentionally conservative. It separates **discovery** (read-only) from
**proposal** (plan for review) from **execution** (gated, verified moves) from **reporting**
(efficiency notes for later). Do not skip the review gate.

## Harness References
- Validation: `scripts/07-validate-harness.sh`, `skills/validate/validate.md`
- Commit (optional, post-approval): `skills/commit/` (`/gitcommit`)
- Telemetry: `telemetry/run-log-schema.md` (record a run if cleanup produces reusable evidence)
- Archive location: `archive/` (repo root)

## Input: $ARGUMENTS
- Optional scope: a path (e.g. `agents/` or `src/voice`) to limit cleanup to one area. Default: whole repo.

## Operating Rules (read before acting)
1. **Archive, never delete.** Move obsolete files to `archive/<original/relative/path>` so they
   remain restorable. Never run `rm` on a tracked file as part of cleanup.
2. **Reference-gate every move.** Before relocating any file, enumerate everything that
   references it: code imports, hardcoded path strings, markdown/links, config keys, scripts,
   CI. Use `git grep -n "<filename>"` (and an IDE find-references for code symbols). Report the
   reference count and risk. **Referenced by code paths or widely linked → update those
   references in the same batch, or stop and warn the user; do not move blind.**
3. **Moves preserve history.** Use `git mv` so renames are tracked and history follows the file.
   For code symbols, prefer IDE/refactor-aware moves so imports update; never blind find-and-replace.
4. **No logic edits.** This skill only moves, consolidates duplicates, and adds comments/docs.
   Any behavioral or performance improvement is *recorded in the final report*, not applied.
5. **Verify in batches.** After each batch of moves, run the test suite and
   `scripts/07-validate-harness.sh`. If scope diverges from intent, halt and reconcile.
6. **Work on a branch.** Confirm a non-default branch; never reorganize directly on `main`.

---

## Step 1 — Discovery (read-only)
Build a complete picture before proposing anything.

- Map the current tree: `git ls-files` plus top-level dirs; note untracked/ignored clutter.
- Identify candidates in these categories:
  - **Duplicates** — same/near-same file content or overlapping configs (`git ls-files | ... md5`).
  - **Redundancies** — superseded scripts, old copies (`*.bak`, `*.old`, `*-copy`, `v2` siblings).
  - **Trailing artifacts** — `__pycache__/`, build debris in tracked paths, stray logs, scratch
    files, screenshots, one-off notes.
  - **Misplaced files** — code/docs/tests/configs sitting in the wrong folder for the project's
    conventions (loose docs at repo root are the most common case).
  - **Obsolete files** — no inbound references and not an entrypoint/asset.
- For each candidate, run `git grep -n "<basename>"` to find references. A file with zero
  references and not an entrypoint/asset is an archive candidate; anything referenced stays
  unless its references move with it.
- Do **not** move anything yet.

## Step 2 — Propose a Plan (review gate)
Present a structured cleanup plan and get user confirmation before touching files. Group by action:

- **Move** (to a better folder): `from → to`, with one-line rationale and reference/risk level.
- **Consolidate** (duplicates/redundancies): which file survives, which is archived, why.
- **Archive** (obsolete): `from → archive/from`, with evidence it's unreferenced.
- **Document** (comments/READMEs to add so structure is self-explanatory).
- **Risk callouts**: list every move that is referenced by code paths or widely linked, with the
  reference list, so the user can judge.

Wait for approval (or scope adjustments) before execution. If the user granted standing autonomy,
proceed but still surface high-risk moves before acting on those specific items.

## Step 3 — Execute (gated, batched)
Apply the approved plan in small, verifiable batches:

1. Ensure `archive/` exists at repo root.
2. For each item, re-confirm references if not just-checked, then move:
   - Code symbols/modules: use IDE/refactor-aware moves so imports/usages update.
   - Non-code (docs, assets, scripts): `git mv` to preserve history; mirror the path under
     `archive/` when archiving.
   - When a moved file is referenced (links, code path strings, configs), update every reference
     in the same batch and re-grep to confirm none remain.
3. Add/update comments and folder `README.md`s so a developer or agent understands each area.
4. Drop an `archive/RESTORE.md` manifest entry per archived file: original path, date, reason,
   and the one-line restore command (`git mv archive/<path> <path>`).
5. After each batch: run the test suite and `scripts/07-validate-harness.sh`. Confirm only the
   expected files/areas are affected. If anything unexpected breaks, revert that batch immediately.

## Step 4 — Verify (no functionality changed)
- `git grep` for every moved file's old path returns no stale references (excluding generated
  mirrors and historical changelogs, which you note rather than rewrite).
- Test suite green (run the project's tests; record exactly what ran and any skips honestly).
- `scripts/07-validate-harness.sh` passes.
- App still boots / imports resolve (smoke-check entrypoints).
- Report any check that was skipped and why — do not claim verification you didn't perform.

## Step 5 — Report
Produce a concise summary:
- **Moved / consolidated / archived** counts with the notable items.
- **Structure now** — short description of the cleaned layout and where things live.
- **Restore instructions** — pointer to `archive/RESTORE.md`.
- **Stale-but-non-breaking references left as-is** — e.g. generated mirrors, historical
  changelogs — listed explicitly so nothing looks silently broken.
- **Efficiency improvements (not applied)** — a prioritized list of behavior/perf/dedup-in-code
  opportunities discovered during cleanup, each with rough effort and risk, to be tackled later
  (e.g. via `/build` after `/plan`).

---

## Definition of Done
- Tree re-organized to professional standards; folders documented.
- Obsolete files archived (restorable), not deleted.
- Duplicates/redundancies/trailing artifacts resolved.
- References updated; verification passed (references + validation + tests); no behavior changed.
- Efficiency-improvement backlog delivered separately from the cleanup itself.
