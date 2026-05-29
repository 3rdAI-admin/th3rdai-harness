---
description: Run an approved application, demo, or harness workflow
---

# Run - Start Approved Runtime Target

Start an application, demo, harness workflow, or eval runtime target in development mode. Follow `configs/tools.yaml` and ask before installing dependencies or starting risky long-running processes.

## Harness References

- Agent: `agents/builder.agent.md`
- Stage: `stages/04-tool-integration/` or `stages/05-evaluation/`
- Tool policy: `configs/tools.yaml`
- Runs: `runs/`
- Telemetry: `telemetry/run-log-schema.md`

## Usage

```text
/run              # Start detected runtime target
/run --build      # Build first, then start if approved
/run --test       # Start with test or eval config
/run <command>    # Run a specific approved command
```

## Auto-Detection

| Target Type | Detection | Candidate Command |
|-------------|-----------|-------------------|
| Python Flask | `app.py` exists | `python app.py` or `flask run` |
| Python FastAPI | `main.py` or app in `pyproject.toml` | `uvicorn main:app --reload` |
| Node.js | `package.json` exists | `npm run dev` or `npm start` |
| React/Vite | `vite.config.*` exists | `npm run dev` |
| Next.js | `next.config.*` exists | `npm run dev` |
| Docker | `docker-compose.yml` exists | `docker-compose up` |
| Harness validation | `scripts/07-validate-harness.sh` exists | `scripts/07-validate-harness.sh` |
| Eval workflow | `evals/` exists | Project-specific eval command or documented manual eval |

## Process

### 1. Detect Run Method

Look for run scripts in order:

1. Explicit user-provided command
2. `package.json` scripts: `dev` → `start` → `serve` → `test`
3. Python: `app.py` → `main.py` → `pyproject.toml` scripts
4. Docker: `docker-compose.yml` → `Dockerfile`
5. Harness: `scripts/07-validate-harness.sh`
6. Eval instructions in `evals/README.md`

### 2. Check Dependencies and Safety

- Verify required dependencies appear to exist, such as `node_modules/` or `venv/`
- Ask before installing dependencies
- Ask before starting long-running servers when user approval is required
- Do not read `.env` directly unless explicitly required and approved
- Prefer `.env.example` for configuration discovery

### 3. Start Target

Run the detected command in the appropriate mode.

For long-running servers:

- Start in the background when supported by the environment
- Report URL, port, process ID, and stop instructions when available
- Check for port conflicts before suggesting destructive process cleanup

### 4. Output

```text
RUNTIME STARTED: <target>

Detected: <framework/workflow>
Command: <command>
URL/process: <url, pid, or N/A>
Validation next step: <check/eval/manual test>

Safety notes:
- <dependencies, secrets, long-running process notes>
```

### 5. Run Record

When useful, record a run under `runs/<run-id>.md` using `telemetry/run-log-schema.md`.

## Orchestrator Execution Mode (opt-in)

The native orchestrator can run a lifecycle route step-by-step instead of only assembling context. This is **opt-in and approval-gated** — dry-run is the default.

```bash
# Dry-run (default): assemble bundles + write skipped records, invoke nothing
python3 scripts/orchestrate.py route <route>

# Execute: run each step through an adapter (still gated)
python3 scripts/orchestrate.py route <route> --execute [--adapter cli|noop] [--max-steps N] [--yes]
```

- **Adapters:** `noop` (default; assembles but executes nothing) or `cli` (shells out to the agent CLI configured in `configs/execution.yaml` → `cli.command`; refuses to run if none is configured). The rendered context bundle is passed to the CLI on stdin; stdout/stderr are captured under `runs/`.
- **Gates (never waived by `--yes`):** a step halts for explicit approval if its adapter command matches a `requires_approval` phrase in `configs/tools.yaml`, or its declared outputs write to a protected path (`agents/`, `configs/`, `scripts/orchestrator/` — the self-modification guard).
- **Per-step checkpoint (waived by `--yes`):** otherwise the driver pauses before each step. Unattended runs with no TTY decline by default, so they stop safely.
- **Runaway guard:** `--max-steps N` caps how many steps run.
- **No autonomous git/installs:** the adapter never commits, installs, or runs destructive commands; those stay human-gated per `configs/tools.yaml` and `CLAUDE.md`. The subprocess runs with a scrubbed env (PATH/HOME/LANG only).

## Stop Command

If running in foreground, the user can stop with Ctrl+C.

If running in background, report the safest available stop command for the specific process.

## Error Handling

- Port already in use: suggest an alternative port or ask before stopping another process
- Missing dependencies: ask before installing
- Build errors: suggest `/build` or `/revise` depending on root cause
- Eval setup missing: document skipped eval and required follow-up
