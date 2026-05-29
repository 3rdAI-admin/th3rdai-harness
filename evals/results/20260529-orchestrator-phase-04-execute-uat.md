# Orchestrator Phase 04 — `--execute` UAT

**Date:** 2026-05-29  
**Verdict:** PASS (plumbing)  
**Config:** `configs/execution.yaml` → `python3 scripts/orchestrator/uat_cli_stub.py`

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

## Notes

- UAT uses a **stdlib stub** so smoke tests do not require API keys; `CliAdapter` passes only `PATH`/`HOME`/`LANG`, which blocks typical agent CLI auth unless credentials live under `HOME` or env passthrough is added later.
- For a **real** model CLI, replace `cli.command` in `execution.yaml` (e.g. `claude -p`) after login; expect to extend env allowlisting if the CLI needs extra environment variables.

## Follow-up

- Optional: add `evals/cases/orchestrator/cli-execute-stub.md` for repeatable rubric scoring.
- Optional: `cli.env_allowlist` in adapter for production agent CLIs.
