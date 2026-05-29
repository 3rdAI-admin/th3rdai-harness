# Plan: Execution Adapter (Opt-In, Approval-Gated)

> **Scope note:** This phase **expands** the Native Orchestrator effort beyond its
> current declared boundary. `EFFORT.md` lists "calling model providers/APIs
> directly, autonomous decision-making" as **out of scope** and describes model
> invocation as the driver's *output* — "a prepared context bundle that a
> human/agent or a **future adapter** executes." This plan specifies that future
> adapter. It is the bridge from *automated bookkeeping* (Phases 01–03) to
> *assisted execution*, and it is the prerequisite for any "build with minimal
> user input" goal. Because it crosses the effort's safety boundary, it is
> opt-in, approval-gated, and dry-run-by-default. Adopting it requires updating
> `EFFORT.md`'s scope statement and phase table (deferred to avoid colliding with
> in-flight Phase 01 work).

## Goal

Add an optional execution layer that takes a sequencer-produced context bundle
(Phase 02) and actually *runs* the step by invoking a reasoning agent, capturing
the real output back into the run record — turning the dry-run coordinator into
an executing driver **without** sacrificing the harness's safety model or its
dependency-free constraint.

## Request Type

feature (harness tooling — execution layer)

## Scope

- In scope:
  - An `Adapter` protocol: `run(bundle) -> StepResult`.
  - A default `CliAdapter` that shells out (stdlib `subprocess`) to an
    already-installed agent CLI, passing the assembled context bundle as the
    prompt and capturing stdout/stderr + exit status as the step result.
  - A `NoopAdapter` preserving today's dry-run behavior (default).
  - An `--execute` flag on `orchestrate.py route` that selects a real adapter;
    absence keeps dry-run.
  - Persisting real `outputs` and `tool_actions` into the run record
    (`telemetry/run-log-schema.md`) instead of `validation.status: skipped`.
  - Per-step **checkpoint**: pause for human approval before the next step.
  - Honoring `configs/tools.yaml` `requires_approval` gates (commits, installs,
    destructive commands, network writes) — these stay human-gated even under
    `--execute`.
  - A bounded loop (`--max-steps`) to prevent runaway execution.
- Out of scope:
  - Bundling provider HTTP SDKs or any pip dependency. (A `urllib`-based HTTP
    adapter is a documented *future* extension, not built here.)
  - Parallel/concurrent step execution.
  - Autonomous git commits or pushes.
  - Self-modification of agent contracts, configs, or this orchestrator's own
    code without explicit approval.

## Harness Context

- Agent(s): Builder (implements), Reviewer (reviews), Evaluator (scores output)
- Depends on: `plans/native-orchestrator/03-cli-and-eval-hook.md` (CLI +
  sequencer + runlog must exist first)
- Config(s): `configs/tools.yaml` (approval gates), `configs/agents.yaml`,
  `configs/models.yaml`; optional new `configs/execution.yaml` for adapter
  selection + CLI command templates
- Telemetry: `telemetry/run-log-schema.md`
- Stage(s): `stages/04-tool-integration/`, `stages/06-iteration/`

## Assumptions

- Phases 01–03 are complete: config loader, runlog writer, sequencer, and CLI
  exist and pass validation.
- A reasoning-agent CLI is available on PATH in the execution environment; the
  command template is configured, never hardcoded.
- Dependency-free constraint still holds: the core and the default `CliAdapter`
  use stdlib only (`subprocess`, `shlex`, `os`, `time`).
- All paths remain repo-root-relative (per `EFFORT.md`); no absolute,
  machine-specific paths are persisted.

## Proposed Approach

`scripts/orchestrator/adapter.py`:

- `class StepResult` (dataclass): `status`, `outputs`, `tool_actions`,
  `stdout_path`, `stderr_path`, `exit_code`, `notes`.
- `class Adapter(Protocol)`: `run(self, bundle: ContextBundle) -> StepResult`.
- `class NoopAdapter`: returns a `skipped` result (current dry-run semantics).
- `class CliAdapter`: renders the bundle to a prompt file, invokes the
  configured CLI via `subprocess.run` with a timeout, captures output to files
  under `runs/`, and maps exit status → `StepResult`. Reads the command template
  from `configs/execution.yaml` (or a documented default); refuses to run if no
  template is configured.
- A small `gates.py` helper that, given a step's intended `tool_actions`,
  checks them against `configs/tools.yaml` `requires_approval` and pauses for an
  interactive yes/no when a gated action is detected.

`scripts/orchestrate.py` (extend Phase 03 CLI):

- Add `route <name> --execute [--adapter cli|noop] [--max-steps N] [--yes]`.
- Default remains dry-run (`noop`). `--execute` requires either interactive
  approval per step or an explicit `--yes` for unattended runs (still subject to
  per-action approval gates).

## Implementation Steps

1. Define `Adapter` protocol + `StepResult` + `NoopAdapter`; wire the sequencer
   to call an adapter so dry-run goes through `NoopAdapter` unchanged.
   (validation: existing dry-run run records are byte-identical in shape)
2. Implement `gates.py` and unit-test it against every `requires_approval` entry
   in `configs/tools.yaml`. (validation: each gated action triggers a prompt;
   non-gated actions do not)
3. Implement `CliAdapter` with configurable command template + timeout + output
   capture; add `configs/execution.yaml` (optional, with a safe disabled
   default). (validation: a stubbed CLI command produces a populated
   `StepResult` and a schema-valid run record with real `outputs`)
4. Extend `orchestrate.py` with `--execute/--adapter/--max-steps/--yes` and the
   per-step checkpoint loop. (validation: `--execute` on a trivial single-step
   route runs the stub, records output, and stops at `--max-steps`)
5. Document the execution mode + safety model in `skills/run/run.md` and
   `README.md`. (validation: skill-reference check still passes)

## Validation Criteria

- [ ] Dry-run (`route <name>`) behavior is unchanged (regression: same run-record shape)
- [ ] `--execute` with a stubbed CLI produces a run record with real `outputs`/`tool_actions`
- [ ] Approval gates from `configs/tools.yaml` trigger before commit/install/destructive/network-write actions
- [ ] `--max-steps` bounds the loop; no runaway
- [ ] No autonomous git commit occurs under any flag
- [ ] No new pip dependency; `python3` stdlib only
- [ ] `scripts/07-validate-harness.sh` still passes

## Safety and Tooling Notes

- **Highest-risk component in the effort.** Default is dry-run; execution is
  strictly opt-in via `--execute`.
- All `configs/tools.yaml` approval gates remain enforced; the adapter never
  bypasses commit/install/destructive/network-write approvals.
- **No self-modification without approval:** the adapter must refuse to let a
  step edit `agents/*`, `configs/*`, or `scripts/orchestrator/*` unless the
  human explicitly approves — to prevent an execution loop from rewriting its
  own contracts or safety policy.
- Bounded by `--max-steps`; per-step checkpoint by default.
- Secrets hygiene: do not pass credentials through the prompt; subprocess
  inherits a minimal, scrubbed env; capture files are written under `runs/` and
  must not log secret values.

## Risks and Edge Cases

- **Runaway / loops** → mitigated by `--max-steps` + per-step checkpoint.
- **Secret leakage** via subprocess env or captured stdout → scrub env, redact,
  document.
- **Non-determinism** of real model output → run records capture exact
  stdout/exit; evals score quality separately (Phase 05 / Evaluator).
- **CLI absent or misconfigured** → `CliAdapter` fails loudly with guidance;
  never silently falls back to a different behavior.
- **Self-modification risk** → explicit refusal + approval gate (see Safety).
- **Scope creep vs `EFFORT.md`** → adoption requires an explicit scope update,
  not a silent expansion.

## Files to Create or Modify

- `plans/native-orchestrator/04-execution-adapter.md` - this plan
- `scripts/orchestrator/adapter.py` - Adapter protocol + Noop/Cli adapters + StepResult
- `scripts/orchestrator/gates.py` - approval-gate checks against tools.yaml
- `scripts/orchestrator/tests/test_adapter.py` - adapter + StepResult tests (stubbed CLI)
- `scripts/orchestrator/tests/test_gates.py` - gate tests against every tools.yaml entry
- `scripts/orchestrate.py` - add `--execute/--adapter/--max-steps/--yes`
- `configs/execution.yaml` - optional adapter selection + CLI command template (disabled by default)
- `skills/run/run.md` - document execution mode + safety model
- `README.md` - note the optional, approval-gated execution mode
- `EFFORT.md` - (deferred) update scope statement + phase table to include Phase 04

## Open Questions

- Adapter selection home: a new `configs/execution.yaml`, or extend
  `configs/tools.yaml`? (Leaning new file to keep tool *policy* separate from
  execution *wiring*.)
- Should `--execute` ever run unattended (`--yes`), or always require per-step
  human approval? (Leaning: `--yes` allowed but per-action gates from
  `tools.yaml` are never waivable.)
- Is a stdlib `urllib` HTTP adapter worth specifying now as a sibling backend,
  or strictly deferred until a CLI-based loop is proven?

## Recommended Next Agent

Reviewer (validate this spec against the plan-quality rubric before any build;
Builder picks it up only after Phases 01–03 are `done`).
