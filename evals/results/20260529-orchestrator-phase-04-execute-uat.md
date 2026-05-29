# Orchestrator Phase 04 — `--execute` UAT

**Date:** 2026-05-29  
**Verdict:** PASS (plumbing)  
**Config:** `configs/execution.yaml` → `claude -p` (scrubbed env + optional `env_allowlist`)

**Stub UAT (2026-05-29 earlier):** `python3 scripts/orchestrator/uat_cli_stub.py` — plumbing only.

## Command

```bash
python3 scripts/orchestrate.py route task_definition --execute --adapter cli --max-steps 1 --yes
```

## Result

| Check | Outcome |
|-------|---------|
| CliAdapter invoked stub CLI | PASS — `validation.status: passed` |
| Run record written | PASS — `runs/20260529-044318-task-definition-01-researcher.md` |
| stdout captured under `runs/` | PASS — `runs/task_definition-01-researcher-stdout.txt` |
| Stub deterministic output | PASS — `orchestrator-uat-stub: ok`, `bundle_chars` present |

## Real CLI verification (2026-05-29)

```bash
python3 scripts/orchestrate.py route task_definition --execute --adapter cli --max-steps 1 --yes
```

| Check | Outcome |
|-------|---------|
| `claude -p` under scrubbed env | PASS — added `USER` to base env; login under `HOME` works |
| Run record | PASS — `runs/20260529-044735-task-definition-01-researcher.md` |
| Model output captured | PASS — stdout under `runs/task_definition-01-researcher-stdout.txt` |

`CliAdapter` base env: `PATH`, `HOME`, `LANG`, `USER`. Optional `cli.env_allowlist` in `execution.yaml` for `ANTHROPIC_API_KEY`, `CURSOR_API_KEY`, etc.

## Follow-up

- Optional: add `evals/cases/orchestrator/cli-execute-stub.md` for repeatable rubric scoring without network.
