# Project Handoff

## Last Updated

**May 30, 2026** — Native Orchestrator Phases 01–04 **done**. Real CLI (`claude -p`) configured and smoke-tested. Harness validator **98/98**; orchestrator tests **70/70**. Dogfood: `iteration` dry-run (3 steps) + `--execute --max-steps 1` PASS. See `evals/results/20260530-orchestrator-dogfood-and-error-handling.md`.

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

1. **Dogfood on a real app** — Bootstrap or attach the harness to a target application; run `task_definition` → `iteration` on actual feature work; record under `runs/` and `evals/results/`.
2. **Multi-step execute** — Try `--max-steps 3` on `iteration` when ready for cost/latency; gates in `configs/tools.yaml` still apply.
3. **Template publish** — Run `scripts/08-prepare-template-release.sh`, enable GitHub **Template repository**, tag `v1.0.0` (see `DISTRIBUTION.md`).

**Limits:** The harness coordinates and optionally shells out to a CLI; it does not autonomously commit, install deps, or bypass approval gates (`CLAUDE.md`, `configs/tools.yaml`).

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
Harness validator:  Passed 98 | Warnings 0 | Failed 0
Orchestrator tests: 70 passed (from repo root)
```

---

## Key Files

| File | Why |
|------|-----|
| `_config/project-notes.md` | This repo's verify commands, CLI, shortcuts |
| `configs/execution.yaml` | `--execute` CLI + env_allowlist |
| `configs/routing.yaml` | Route names |
| `scripts/orchestrate.py` | CLI entry |
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
Resume th3rdai-harness. Read HANDOFF.md and _config/project-notes.md.

State: Orchestrator 01–04 done; claude -p configured; validator 98/98; 70 tests. Dogfood iteration dry-run + execute step 1 PASS (evals/results/20260530-orchestrator-dogfood-and-error-handling.md).

Next: bootstrap harness onto a real application repo OR run multi-step --execute on a feature. Do not commit without approval. Update Archon when done.
```
