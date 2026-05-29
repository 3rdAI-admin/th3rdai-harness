# Plan: Execution Adapter (opt-in)

## Goal

Close the coordinator→executor gap. Take a context bundle from the sequencer (Phase 02), hand it to an external agent runtime that performs the step in a real target workspace, capture the produced artifacts, thread them into the next step's inputs, run the eval hook as a pass/retry/stop **gate**, and record a run with a real verdict. This is the piece that turns the automated *bookkeeping* of 01–03 into minimal-intervention *execution*.

## Request Type

feature (harness tooling) — **crosses the coordinator/executor boundary; opt-in only**

## Relationship to the Core (01–03)

Phases 01–03 are coordinator-only: dependency-free, dry-run, no model/network. **Phase 04 is the single, opt-in exception** that may take a runtime dependency and touch model/network/filesystem. It lives behind an explicit flag (`orchestrate run <route> --execute`) and is never the default. The core's purity guarantees remain intact for 01–03 — they import nothing from this phase — and all dependency/network behavior is quarantined in `executor.py`.

## Scope

- In scope: a pluggable **executor interface** (bundle in → artifacts + transcript out); one concrete backend wrapping an existing agent runtime (e.g. Claude Code headless or the Claude Agent SDK); a real **target workspace** the executor writes into; **artifact threading** between steps; wiring the Phase 03 eval hook as a per-step **gate** (pass / bounded-retry / stop); run records with a real `validation.status`; enforcement of the checkpoint policy for commit/install/destructive operations per `configs/tools.yaml` + `CLAUDE.md`.
- Out of scope: building a bespoke agent loop or model client from scratch (wrap a mature runtime instead); replacing the 01–03 dry-run path (execute mode is purely additive); auto-approving gated operations; networked/distributed execution across machines.

## Harness Context

- Agent(s): Builder (implements), Reviewer (reviews), Evaluator (gate verdicts)
- Depends on: `01-config-and-runlog.md`, `02-sequencer.md`, `03-cli-and-eval-hook.md`
- Config(s): `configs/tools.yaml` (approval policy), `configs/models.yaml` (backend/model selection), `configs/routing.yaml`
- Telemetry: `telemetry/run-log-schema.md`
- Stage(s): `stages/04-tool-integration/`, `stages/05-evaluation/`, `stages/06-iteration/`

## Assumptions

- An external runtime is available and authorized (Claude Code headless or Agent SDK). Its invocation is the only networked, dependency-bearing part of the whole system.
- The target app/workspace is a **separate directory** (configurable, repo-relative or `PROJECT_ROOT`-anchored), never the harness repo itself.
- Human approval remains required for commit/install/destructive operations (per `CLAUDE.md` and `configs/tools.yaml`) even in execute mode — this is "minimal intervention," not zero.
- Import/package conventions follow `01-config-and-runlog.md` → *Package & Import Convention* (`from orchestrator import ...`, no `from .`).

## Proposed Approach

`scripts/orchestrator/executor.py`:

- `Executor` protocol — `run(bundle, workspace) -> StepResult` (produced/modified artifacts, transcript/log, status). Backend-agnostic so the harness stays model-agnostic; the runtime wrapper is one implementation, not the contract.
- `RuntimeExecutor` — a concrete `Executor` that invokes an existing agent runtime with the bundle as its instruction and the target workspace as its working directory, then captures the files it produced and the transcript.
- `gate(step_result) -> verdict` — reuses the Phase 03 eval hook: assemble case + rubric, obtain the verdict, and decide **pass / retry (bounded) / stop**.
- Sequencer gains an `--execute` path: for each step, `build_context` (02) → `Executor.run` (04) → thread artifacts into the next step's inputs → `gate` → write a run record with the real status. On a gate-stop or any gated operation, halt and surface to the human.

## Implementation Steps

1. Define the `Executor` protocol + `StepResult`, and wire an `--execute` flag through the CLI (default off). (validation: `orchestrate --help` shows execute mode; omitting the flag preserves dry-run exactly)
2. Implement `RuntimeExecutor` against one runtime, running in an isolated target workspace; capture artifacts + transcript. (validation: a one-step bundle produces real files in the workspace and a populated, non-skipped run record)
3. Thread step N artifacts into step N+1 inputs; add the eval gate with bounded retry. (validation: a 2-step route passes artifacts forward and records a real verdict per step)
4. Enforce the checkpoint policy: a step requesting a commit/install/destructive op pauses for approval. (validation: such a step halts and surfaces to the human instead of proceeding)

## Validation Criteria

- [ ] Execute mode is opt-in; omitting `--execute` preserves the 01–03 dry-run behavior exactly (no deps, no network)
- [ ] A full lifecycle route runs end-to-end against a sample spec, producing a working artifact in the target workspace with real (non-skipped) run records
- [ ] The eval gate threads and blocks correctly — a failing step triggers retry or stop, never a silent pass
- [ ] Gated operations (commit/install/destructive) require human approval per `configs/tools.yaml`
- [ ] Core invariants for 01–03 unchanged: `scripts/07-validate-harness.sh` passes and the dry-run path needs no dependencies

## Safety and Tooling Notes

- This is the **only** component permitted network/model access and an external dependency; all of it is gated behind the execute flag and isolated in `executor.py`.
- It never auto-approves commit/install/destructive operations — the autonomy ceiling is the checkpoint policy, by design.
- The target workspace is separate from the harness repo; the executor never writes harness internals during an app build.

## Risks and Edge Cases

- Runaway/looping executor → bounded retries plus a hard per-route step cap.
- Non-deterministic model output → run records capture transcript + artifacts for reproducibility; the eval gate enforces quality.
- Backend lock-in → mitigated by the pluggable `Executor` interface; the runtime wrapper is one implementation.
- Dependency creep into the core → enforced by keeping all runtime/network code in `executor.py` behind the flag; 01–03 import nothing from it.

## Files to Create or Modify

- `scripts/orchestrator/executor.py` - `Executor` protocol + `RuntimeExecutor` + gate wiring
- `scripts/orchestrator/sequencer.py` - add the `--execute` path (artifact threading + gate)
- `scripts/orchestrate.py` - expose `run <route> --execute`
- `scripts/orchestrator/tests/test_executor.py` - executor + gate tests (stubbed runtime, no network)
- `README.md` - document execute mode and its opt-in, dependency-bearing nature

## Open Questions

- Which runtime is the first backend — Claude Code headless CLI vs Claude Agent SDK? Both satisfy the interface; pick by ease of artifact/transcript capture.
- Where does the target workspace live, and how is it reset between runs?
- Is the gate verdict model-scored in this phase (needs the runtime) or still human/agent-entered, with model scoring deferred?

## Recommended Next Agent

Reviewer
