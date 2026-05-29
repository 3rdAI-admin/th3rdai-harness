# Plan: Stage/Agent Sequencer (Dry-Run)

## Goal

Compute the intended agent/stage sequence from config and assemble a per-step context bundle, without executing any model.

## Request Type

feature (harness tooling)

## Scope

- In scope: resolve a lifecycle route into ordered steps; for each step gather the agent contract, default skill procedure, prompt version, model profile, and declared inputs into a context bundle; dry-run output + run record per step.
- Out of scope: calling an LLM/provider, making decisions, parallel execution.

## Harness Context

- Agent(s): Builder, Reviewer
- Depends on: `plans/native-orchestrator/01-config-and-runlog.md`
- Config(s): `configs/routing.yaml`, `configs/agents.yaml`, `configs/models.yaml`
- Prompts: `prompts/registry.md`
- Telemetry: `telemetry/run-log-schema.md`

## Assumptions

- Builds on `01-config-and-runlog.md` and its *Package & Import Convention* (`from orchestrator import ...`, no `from .`).
- Each route in `routing.yaml` maps to one `stage:` and an ordered `agents:` list; every listed agent resolves in `agents.yaml`.
- **Prompt version** is resolved from `prompts/registry.md` (the *Current Version* column keyed by *Agent*; all five agents currently map to `<agent>/v1.md`); fallback is the latest `prompts/<agent>/vN.md`. `agents.yaml` carries no prompt field, so the registry/convention is the single source. An agent with no prompt records `prompt_version: null`.
- A step's **declared inputs/outputs** come from its stage contract `stages/NN/CONTEXT.md`, not from `agents.yaml`.
- Dry-run is the only mode in this phase; the opt-in `--execute` mode arrives in Phase 04. Records use `validation.status: skipped`.

## Proposed Approach

`scripts/orchestrator/sequencer.py`:

- `plan_route(route_name) -> [Step]` reads `routing.yaml` for the stage + ordered agents; resolves each agent via `agents.yaml` to contract, `default_skill`, and `model_profile`.
- `build_context(step) -> ContextBundle` assembles a plain-text bundle (paths + content pointers, not LLM output) from defined sources: the **contract** and **default_skill** from `agents.yaml`; the **prompt version** from `prompts/registry.md` (fallback latest `prompts/<agent>/vN.md`, else `null`); the **model profile** from `agents.yaml` → `configs/models.yaml`; and the step's **declared inputs/outputs** from its stage contract `stages/NN/CONTEXT.md`.
- Dry-run mode prints the bundle and writes a run record marking `validation.status: skipped` (dry run).

## Implementation Steps

1. Implement `plan_route` over `routing.yaml`; assert every referenced agent resolves. (validation: routes for all 7 stages produce non-empty, contract-backed steps)
2. Implement `build_context`; resolve each field from its defined source and gracefully report any missing referenced file. (validation: bundle lists contract + procedure + prompt version + model profile + stage-contract inputs for each step, recording `null` where a source is genuinely absent)
3. Emit a dry-run run record per step via `runlog.write`. (validation: records validate against the schema)

## Validation Criteria

- [ ] `plan_route` resolves all stages in `routing.yaml` with contract-backed agents
- [ ] `build_context` resolves prompt version (registry/convention) and declared inputs (stage contract) per step, recording `null` when genuinely absent
- [ ] Missing referenced files are reported, not silently skipped
- [ ] Dry-run produces schema-valid run records under `runs/`
- [ ] `scripts/07-validate-harness.sh` still passes

## Safety and Tooling Notes

- Dry-run by default; coordinator never invokes a model or network.
- Read-only except run records.

## Risks and Edge Cases

- An agent with `default_skill: null` (none currently) → step records "no skill" rather than crashing.
- Routing references an undefined agent → fail loudly (already fail-checked by the validator).

## Files to Create or Modify

- `scripts/orchestrator/sequencer.py` - route planning + context assembly
- `scripts/orchestrator/tests/test_sequencer.py` - tests

## Recommended Next Agent

Reviewer
