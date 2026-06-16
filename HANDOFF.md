# Project Handoff

## Last Updated

**June 16, 2026** — ICM Phase 1 **done**. Distribution modes, conventions, quick reference, release validation added. Native Orchestrator Phases 01–04 **done**. Real CLI (`claude -p`) configured. Harness validator **100/100**; orchestrator tests **70/70**. **Template release ready.**

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

1. **Template publish** — Enable GitHub **Template repository**, tag `v1.0.0`, publish release (see `DISTRIBUTION.md`). Release validation passed ✓.
2. **Dogfood on a real app** — Bootstrap or attach the harness to a target application; run `task_definition` → `iteration` on actual feature work; record under `runs/` and `evals/results/`.
3. **Multi-step execute** — Try `--max-steps 3` on `iteration` when ready for cost/latency; gates in `configs/tools.yaml` still apply.

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

State: ICM Phase 1 done (distribution, conventions, quick ref). Orchestrator 01–04 done. Validator 100/100; orchestrator 70/70; bootstrap test passed. **Template release ready.**

Next: Publish v1.0.0 template (enable GitHub Template repository, tag release) OR dogfood on real app. Do not commit without approval. Update Archon when done.
```
