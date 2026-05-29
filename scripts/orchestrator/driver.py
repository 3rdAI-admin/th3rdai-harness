"""Execute-mode driver for the opt-in execution layer (Phase 04).

Runs a lifecycle route step-by-step through an :class:`adapter.Adapter`, enforcing
the safety model before each step and recording a real run record per step:

- **Approval gates (never waived by ``assume_yes``):** if a step's adapter command
  matches a ``requires_approval`` phrase in ``configs/tools.yaml``, or its declared
  outputs write to a protected path (``agents/``, ``configs/``,
  ``scripts/orchestrator/`` — the self-modification guard), the driver prompts for
  explicit approval and halts the run if it is not granted.
- **Per-step checkpoint (waived by ``assume_yes``):** otherwise the driver pauses
  before each step unless ``assume_yes`` is set.
- **Bounded:** ``max_steps`` caps how many steps run, preventing runaway loops.

Coordinator discipline still holds: the driver itself never reasons or calls a
model — it asks the adapter to run the step and records the outcome. With
``NoopAdapter`` it executes nothing (dry-run semantics); with ``CliAdapter`` it
shells out to a configured CLI. Stdlib only; absolute imports.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from scripts.orchestrator import config, gates, runlog, sequencer  # noqa: F401


def _execute_record(step, bundle, result, now: datetime) -> runlog.RunRecord:
    run_id = runlog.new_run_id(f"{step.route}-{step.order:02d}-{step.agent}", now=now)
    inputs = [p for p in (bundle.contract, bundle.skill, bundle.prompt_version,
                          bundle.stage_contract) if p]
    inputs.extend(bundle.inputs)

    status_map = {"executed": "passed", "failed": "failed", "skipped": "skipped"}
    issues = [
        {"severity": "medium", "description": f"missing referenced file: {m}"}
        for m in bundle.missing
    ]
    if result.status == "failed":
        issues.append({"severity": "high", "description": result.notes or "step failed"})

    return runlog.RunRecord(
        run_id=run_id,
        created_at=now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        request=f"Execute step {step.order} of route '{step.route}': {step.agent} @ {step.stage}",
        agent=step.agent,
        skill=step.default_skill,
        prompt_version=bundle.prompt_version,
        model_profile=step.model_profile,
        inputs=inputs,
        outputs=list(result.outputs),
        tool_actions=list(result.tool_actions),
        validation={"status": status_map.get(result.status, "failed"), "notes": result.notes},
        issues=issues,
        follow_up=(["review captured output"] if result.status != "skipped"
                   else ["run with --execute and a configured adapter to execute this step"]),
    )


def _blockers(adapter, bundle):
    """Actions on this step that require explicit (non-waivable) approval."""
    command = getattr(adapter, "command", None)
    cmd_actions = [" ".join(command)] if command else []
    gated = gates.gated_actions(cmd_actions)
    protected = gates.protected_writes(bundle.outputs)
    return gated, protected


def execute_route(route_name: str, adapter, runs_dir: str = "runs",
                  max_steps: Optional[int] = None, assume_yes: bool = False,
                  prompt_fn=input, out=print, now: Optional[datetime] = None) -> list:
    """Run a route through ``adapter``, gating and recording each step.

    Returns a list of ``(step, StepResult, RunRecord, path)`` for steps that ran.
    Stops early (returning what ran so far) on an unapproved gate or checkpoint.
    """
    now = now or datetime.now(timezone.utc)
    steps = sequencer.plan_route(route_name)
    if max_steps is not None:
        steps = steps[:max_steps]

    results = []
    for step in steps:
        bundle = sequencer.build_context(step)
        gated, protected = _blockers(adapter, bundle)

        if gated or protected:
            detail = []
            if gated:
                detail.append(f"gated action(s): {', '.join(gated)}")
            if protected:
                detail.append(f"protected write(s): {', '.join(protected)}")
            reply = prompt_fn(
                f"Step {step.order} ({step.agent} @ {step.stage}) requires approval — "
                f"{'; '.join(detail)}. Approve? [y/N] "
            )
            if str(reply).strip().lower() not in ("y", "yes"):
                out(f"halted before step {step.order} ({step.agent}): approval not granted "
                    f"({'; '.join(detail)})")
                break
        elif not assume_yes:
            reply = prompt_fn(
                f"Proceed with step {step.order}: {step.agent} @ {step.stage}? [y/N] "
            )
            if str(reply).strip().lower() not in ("y", "yes"):
                out(f"stopped before step {step.order} ({step.agent}) by user")
                break

        result = adapter.run(
            bundle, runs_dir=runs_dir,
            label=f"{step.route}-{step.order:02d}-{step.agent}",
        )
        record = _execute_record(step, bundle, result, now)
        path = runlog.write(record, dir=runs_dir)
        results.append((step, result, record, path))

    return results
