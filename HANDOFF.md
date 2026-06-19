# Project Handoff

## Last Updated

**June 19, 2026** — v1.1.0 **COMPLETE**. GitNexus code-cleanup integration shipped: `/code-cleanup` skill now uses explicit `gitnexus_impact()` and `gitnexus_detect_changes()` calls for precise blast-radius analysis. HIGH/CRITICAL risk triggers hard stop. Hybrid approach (GitNexus for code files, git grep for non-code). Complete harness workflow demonstrated (dogfooding): Task Definition → Planning → Evaluation (5.0/5.0) → Implementation → Release. Validation: 100/100 harness, 70/70 orchestrator tests. Tagged v1.1.0, ready to push. Repository stable and production-ready.

---

## Resume Here (next session)

Read: this file → `_config/project-notes.md` → `README.md` → `VERSION3.md` → `plans/native-orchestrator/EFFORT.md`.

**Verify green:**

```bash
scripts/07-validate-harness.sh
python3 -m unittest discover scripts/orchestrator/tests
```

**Orchestrator:**

```bash
python3 scripts/orchestrate.py route iteration --dry-run
python3 scripts/orchestrate.py route iteration --execute --adapter cli --max-steps 1 --yes
python3 scripts/orchestrate.py eval evals/cases/orchestrator/config-subset-parsing.md
```

**Pick up in priority order:**

1. ✅ **v1.0.0 Released** — Template repository enabled, GitHub release published (June 19, 2026). See `RELEASE-STATUS.md`.
2. ✅ **v1.1.0 Complete** — GitNexus code-cleanup integration shipped. Task `56c035fb-8701-493f-802a-30e14c6ffca9` marked done in Archon. See `stages/06-iteration/output/iteration-notes.md` for complete implementation record. Tagged v1.1.0, ready to push to GitHub.
3. **Dogfood on real app** — Bootstrap or attach the harness to a target application; run `task_definition` → `iteration` on actual feature work; record under `runs/` and `evals/results/`.
4. **Multi-step execute** — Try `--max-steps 3` on `iteration` when ready for cost/latency; gates in `configs/tools.yaml` still apply.

**Limits:** The harness coordinates and optionally shells out to a CLI; it does not autonomously commit, install deps, or bypass approval gates (`CLAUDE.md`, `configs/tools.yaml`).

---

## ICM Pedagogical Enhancements

**Phase 1 completed June 16, 2026** (commits 7ef2d98, 1e3bd6e, 4169036):

- **Distribution modes:** README "Use This Harness" section, enhanced `scripts/01-create-project.sh` with `--with-orchestrator` and non-interactive mode
- **Release automation:** `scripts/08-prepare-template-release.sh` (validator + orchestrator tests + bootstrap dry-run)
- **Navigation:** `docs/QUICK-REFERENCE.md` (5-layer model, commands, lifecycle, pitfalls)
- **Standards:** `_config/conventions.md` (naming, file conventions, load indicators, commit format)
- **Testing permissions:** `.claude/settings.json` (pre-approved development commands)

**Validation:** 100 passed, 2 optional warnings (security-baseline forward reference, token budgets deferred to Phase 2).

**Phase 2 (optional, deferred):** Token budget columns (`Tokens (est.)`) in stage CONTEXT.md files.

---

## Native Orchestrator Status

| Phase | Deliverable | Status |
|-------|-------------|--------|
| 01 | Config + runlog | **done** |
| 02 | Sequencer (dry-run bundles) | **done** |
| 03 | CLI + eval hook | **done** |
| 04 | Execution adapter (`--execute`) | **done** — `claude -p` in `configs/execution.yaml` |

**Evals:** Phases 01–03 PASS 5.0/5.0 (`evals/results/20260529-orchestrator-phase-01-03-validation.md`). Phase 04 spec + execute UAT (`evals/results/20260529-orchestrator-phase-04-validation.md`, `20260529-orchestrator-phase-04-execute-uat.md`). Dogfood 2026-05-30 (`evals/results/20260530-orchestrator-dogfood-and-error-handling.md`).

**Orchestrator cases (8):** `config-subset-parsing`, `run-record-fidelity`, `route-context-bundle`, `malformed-config`, `missing-references`, `invalid-route`, `phase-04-timeout-handling`, `phase-04-execute-real-cli` — all under `evals/cases/orchestrator/`.

---

## Validation (current)

```text
Harness validator:  Passed 100 | Warnings 2 (optional) | Failed 0
Orchestrator tests: 70 passed (from repo root)
Bootstrap test:     ✓ Passed (scripts/08-prepare-template-release.sh)
```

---

## Key Files

| File | Why |
|------|-----|
| `DISTRIBUTION.md` | How to consume/publish template (GitHub, local, attach modes) |
| `docs/QUICK-REFERENCE.md` | Fast lookup: 5-layer navigation, commands, lifecycle |
| `_config/conventions.md` | Naming standards, file conventions, load indicators |
| `_config/project-notes.md` | This repo's verify commands, CLI, shortcuts |
| `configs/execution.yaml` | `--execute` CLI + env_allowlist |
| `configs/routing.yaml` | Route names |
| `scripts/orchestrate.py` | CLI entry |
| `scripts/08-prepare-template-release.sh` | Pre-release validation (harness + orchestrator + bootstrap) |
| `FRAMEWORK.md` | Conceptual model + deployment overlay |

---

## Important Notes

- **Commits** require explicit human approval (`CLAUDE.md`).
- **Archon:** project **Th3rdai-Harness** (`eb8b4363-b1f0-4448-8e71-c557e0daa5b2`).
- **GitNexus:** impact analysis before editing symbols; `npx gitnexus analyze` after structural changes.
- **Portable skills:** deployment detail lives in `_config/project-notes.md`, not in `skills/*`.

---

## Suggested Next Agent Prompt

```text
Resume th3rdai-harness. Read HANDOFF.md.

State: v1.1.0 **COMPLETE** (June 19, 2026). GitNexus code-cleanup integration shipped. `/code-cleanup` skill now uses `gitnexus_impact()` for blast-radius analysis, `gitnexus_detect_changes()` for verification. Full harness workflow demonstrated (dogfooding). Tagged v1.1.0, ready to push to GitHub.

Options:
1. Push v1.1.0 — Push main + tags to GitHub, optionally create GitHub release
2. Dogfood — Apply harness to real app (bootstrap or attach mode)
3. Multi-step execute — Test orchestrator on complex routes

Do not commit without approval. Update Archon when done.
```
