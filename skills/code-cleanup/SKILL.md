# Skill: code-cleanup

Invoked by: `/code-cleanup` command (a.k.a. **Code Cleanup**)

## Procedure

Load and follow `skills/code-cleanup/code-cleanup.md` when executing this skill.

## Purpose
Review a repository for cleanup and re-organize it to a professional, industry-standard
layout **without impacting or breaking any functionality or capabilities**. Files that are
no longer necessary are *archived* (moved to `archive/`), never deleted, so anything can be
restored if an issue surfaces. Duplicates, redundancies, and trailing artifacts are
consolidated, files are moved to appropriate folders, and the result is documented so a
developer or agent can understand the codebase.

## When to Use
- The repo has accumulated stray files, scratch scripts, duplicate configs, or ad-hoc folders
- Before a release or handoff, to present a clean, navigable structure
- After a burst of rapid iteration that left the tree disorganized
- Anytime the user asks to "clean up", "re-organize", or "tidy" the codebase

## Output
- A **cleanup plan** (proposed moves/archives/consolidations) presented for review before changes
- Files moved to appropriate folders; obsolete-but-restorable files relocated to `archive/` with a manifest
- Updated comments / READMEs so structure is self-explanatory
- A verification report confirming **no functionality changed** (references checked, tests run)
- A list of **efficiency improvements** to apply *after* cleanup (recommendations only, not applied)

## Safety Contract (Never Break Functionality)
- **Archive, don't delete.** Obsolete files move to `archive/` preserving their relative path.
- **Reference-gate every move.** Before relocating any file, find everything that references it
  (code imports, path strings, links, configs, scripts). If a move would break a reference,
  update the reference in the same batch or do not move the file. Surface anything high-risk.
- **Verify after each batch.** Run the test suite and `scripts/07-validate-harness.sh`; only
  proceed if scope matches intent.
- **No behavior edits.** This skill moves, consolidates, and documents — it does not refactor
  logic. Logic improvements are *noted*, not applied.

## Harness References
- Procedure: `skills/code-cleanup/code-cleanup.md`
- Validation: `skills/validate/validate.md`, `scripts/07-validate-harness.sh`
- Commit (optional, after approval): `skills/commit/` (`/gitcommit`)
- Archive location: `archive/` (repo root)

## Next Step
- Success: run `/validate` (or the project test suite) to confirm health, then commit on a branch.
- If reference analysis flags a high-risk move (widely referenced, or referenced by code paths):
  stop, report the blast radius, and hand back to the user for a decision.
