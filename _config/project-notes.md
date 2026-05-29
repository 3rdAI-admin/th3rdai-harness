# Project Notes (deployment overlay)

This file is **project-specific**. It is not part of the portable harness contract.
Generic skills (`skills/research/`, `skills/debug/`, `skills/validate/`, etc.) stay
application-agnostic; read this file when working **in this repository** for local
commands, optional tooling, and resume context.

Bootstrapped projects should replace this content (see `_config/project-notes.TEMPLATE.md`).

---

## Project

**Name:** th3rdai-harness (AI Agent Development Harness)  
**Tracking:** Archon project **Th3rdai-Harness**

## Resume (read first when returning)

1. `HANDOFF.md`
2. `README.md` (orchestrator CLI section)
3. `VERSION3.md`
4. `plans/native-orchestrator/EFFORT.md`

## Verify green (this repo)

```bash
scripts/07-validate-harness.sh
python3 -m unittest discover scripts/orchestrator/tests
```

Latest known targets (capture actual output — counts may change):

```text
Harness validator:  Passed 93 | Warnings 0 | Failed 0
Orchestrator tests: 69 passed (from repo root)
```

## Optional Native Orchestrator

Present in this repo only if these paths exist:

- `scripts/orchestrate.py`, `scripts/orchestrator/`
- `plans/native-orchestrator/`
- `evals/rubrics/orchestrator-output-quality.md`
- `evals/cases/orchestrator/`

**CLI:**

```bash
python3 scripts/orchestrate.py --help
python3 scripts/orchestrate.py route <route-name> --dry-run
python3 scripts/orchestrate.py eval evals/cases/orchestrator/<case>.md
python3 scripts/orchestrate.py route <route-name> --execute --adapter cli --max-steps 1
```

Routes: `task_definition`, `agent_design`, `prompt_design`, `tool_integration`, `evaluation`, `iteration`, `release` (`configs/routing.yaml`).

**Phase status (EFFORT.md):** 01–04 done. `configs/execution.yaml` uses `claude -p` for `--adapter cli`; UAT stub at `scripts/orchestrator/uat_cli_stub.py` for offline plumbing checks.

**Import convention:** `from scripts.orchestrator import ...`; run tests from repo root.

**Formal eval result:** `evals/results/20260529-orchestrator-phase-01-03-validation.md` (PASS 5.0/5.0).

## Research shortcuts (this repo)

- Orchestrator status → `plans/native-orchestrator/EFFORT.md`
- Eval inventory → `evals/README.md`
- Routing → `configs/routing.yaml`

## Debug shortcuts (this repo)

| Symptom | Likely repro |
|---------|----------------|
| Orchestrator import error | Wrong cwd or `from orchestrator` instead of `scripts.orchestrator` |
| Config `[]` parsed as string | `configs/tools.yaml` `requires_approval: []` — see `evals/cases/orchestrator/config-subset-parsing.md` |
| Route bundle incomplete | `python3 scripts/orchestrate.py route iteration --dry-run` |

## Run skill (orchestrator execution)

See **Optional Native Orchestrator** above for `route --execute`, adapters (`noop`/`cli`), approval gates, `--max-steps`, and self-modification guard on `agents/`, `configs/`, `scripts/orchestrator/`.

## Eval skill (CLI scaffold)

```bash
python3 scripts/orchestrate.py eval evals/cases/<category>/<case>.md [--rubric evals/rubrics/<name>.md]
```

Writes PENDING `evals/results/` stub + run record; Evaluator still scores manually.

## Plan / build / release notes (this repo)

- Plans live under `plans/`; native orchestrator effort: `plans/native-orchestrator/`
- After build: run verify commands in **Verify green** above
- Before commit: confirm `evals/results/20260529-orchestrator-phase-01-03-validation.md` not blocking if releasing orchestrator work

## Open decisions (this repo)

- **Agent CLI:** default `claude -p`; add keys under `cli.env_allowlist` in `execution.yaml` if your CLI needs extra env vars (base: PATH, HOME, LANG, USER).
