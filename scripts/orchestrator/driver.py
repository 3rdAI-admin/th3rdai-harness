"""Execute-mode driver for the opt-in execution layer (Phase 04 + v1.2.0 Autonomy).

Runs a lifecycle route step-by-step through an :class:`adapter.Adapter`, enforcing
the safety model before each step and recording a real run record per step:

- **Approval gates (never waived by ``assume_yes``):** if a step's adapter command
  matches a ``requires_approval`` phrase in ``configs/tools.yaml``, or its declared
  outputs write to a protected path (``agents/``, ``configs/``,
  ``scripts/orchestrator/`` — the self-modification guard), the driver prompts for
  explicit approval and halts the run if it is not granted.
- **Per-step checkpoint (waived by ``assume_yes``):** otherwise the driver pauses
  before each step unless ``assume_yes`` is set.
- **Autonomy gates (v1.2.0):** when autonomy mode is configured, risk-based approval
  gates apply. LOW/MEDIUM auto-approved in cautious mode, HIGH requires approval,
  CRITICAL blocked. See ``configs/autonomy.yaml`` and ``autonomy_manager.py``.
- **Bounded:** ``max_steps`` caps how many steps run, preventing runaway loops.

Coordinator discipline still holds: the driver itself never reasons or calls a
model — it asks the adapter to run the step and records the outcome. With
``NoopAdapter`` it executes nothing (dry-run semantics); with ``CliAdapter`` it
shells out to a configured CLI. Stdlib only; absolute imports.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from scripts.orchestrator import config, gates, runlog, sequencer  # noqa: F401

# Import AutonomyManager (graceful fallback if not available)
try:
    from scripts.orchestrator.autonomy_manager import AutonomyManager
    AUTONOMY_AVAILABLE = True
except ImportError:
    AUTONOMY_AVAILABLE = False
    AutonomyManager = None


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


def _classify_step_risk(step, bundle, adapter, autonomy_manager) -> str:
    """
    Classify step risk using AutonomyManager heuristics.

    Args:
        step: Sequencer step
        bundle: Context bundle
        adapter: Execution adapter
        autonomy_manager: AutonomyManager instance

    Returns:
        Risk level (LOW|MEDIUM|HIGH|CRITICAL)
    """
    if not autonomy_manager:
        return "MEDIUM"  # Safe default when autonomy unavailable

    # Check for protected writes (self-modification = HIGH risk)
    if gates.protected_writes(bundle.outputs):
        return "HIGH"

    # Check for gated actions (requires approval = HIGH risk)
    command = getattr(adapter, "command", None)
    cmd_actions = [" ".join(command)] if command else []
    if gates.gated_actions(cmd_actions):
        return "HIGH"

    # Use heuristic classification based on operation description
    operation_desc = f"{step.agent} @ {step.stage}"
    return autonomy_manager.classify_operation_heuristic(operation_desc)


def execute_route(route_name: str, adapter, runs_dir: str = "runs",
                  max_steps: Optional[int] = None, assume_yes: bool = False,
                  autonomy_mode: Optional[str] = None,
                  prompt_fn=input, out=print, now: Optional[datetime] = None) -> list:
    """Run a route through ``adapter``, gating and recording each step.

    Args:
        route_name: Name of route from configs/routing.yaml
        adapter: Execution adapter (NoopAdapter or CliAdapter)
        runs_dir: Directory for run records
        max_steps: Cap on number of steps to execute
        assume_yes: Skip per-step checkpoints (gates still apply)
        autonomy_mode: Autonomy mode override (ask|cautious|full) or None for config default
        prompt_fn: Function for user prompts (default: input)
        out: Output function (default: print)
        now: Timestamp override for testing

    Returns:
        List of ``(step, StepResult, RunRecord, path)`` for steps that ran.
        Stops early (returning what ran so far) on an unapproved gate or checkpoint.
    """
    now = now or datetime.now(timezone.utc)
    steps = sequencer.plan_route(route_name)
    if max_steps is not None:
        steps = steps[:max_steps]

    # Initialize AutonomyManager if available and config exists
    autonomy_manager = None
    if AUTONOMY_AVAILABLE and (config.repo_root() / "configs" / "autonomy.yaml").exists():
        try:
            autonomy_manager = AutonomyManager(mode_override=autonomy_mode)
            out(f"Autonomy mode: {autonomy_manager.mode} ({autonomy_manager.get_mode_description()})")
        except Exception as e:
            out(f"Warning: autonomy config error ({e}); proceeding with manual approval")

    results = []
    for step in steps:
        bundle = sequencer.build_context(step)
        gated, protected = _blockers(adapter, bundle)

        # Classify risk for autonomy gates
        risk_level = _classify_step_risk(step, bundle, adapter, autonomy_manager)

        # Build context for audit log
        context = {
            "step": step.order,
            "agent": step.agent,
            "stage": step.stage,
            "outputs": list(bundle.outputs),
            "gated": list(gated) if gated else [],
            "protected": list(protected) if protected else []
        }

        # Check autonomy gates if AutonomyManager available
        if autonomy_manager:
            should_ask, reason, action = autonomy_manager.should_request_approval(
                operation=f"{step.agent} @ {step.stage}",
                risk_level=risk_level,
                context=context
            )

            # CRITICAL blocked in cautious mode
            if action == "block":
                out(f"❌ BLOCKED: Step {step.order} ({step.agent})")
                out(f"   Risk: {risk_level}")
                out(f"   Reason: {reason}")
                autonomy_manager.save_audit_log()
                break

            # Auto-approved (proceed without prompt)
            if action == "proceed":
                out(f"✓ Step {step.order} ({step.agent}): {risk_level} risk auto-approved")
                # Continue to execution below

            # Ask for approval
            elif action == "ask":
                detail = [f"risk: {risk_level}"]
                if gated:
                    detail.append(f"gated: {', '.join(gated)}")
                if protected:
                    detail.append(f"protected: {', '.join(protected)}")

                reply = prompt_fn(
                    f"Step {step.order} ({step.agent} @ {step.stage}) — "
                    f"{'; '.join(detail)}. Approve? [y/N] "
                )
                approved = str(reply).strip().lower() in ("y", "yes")
                autonomy_manager.log_user_decision(
                    f"{step.agent} @ {step.stage}",
                    risk_level,
                    approved,
                    context
                )

                if not approved:
                    out(f"halted before step {step.order} ({step.agent}): approval not granted")
                    autonomy_manager.save_audit_log()
                    break

        # Legacy approval gates (when autonomy unavailable)
        else:
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

        # Execute the step
        result = adapter.run(
            bundle, runs_dir=runs_dir,
            label=f"{step.route}-{step.order:02d}-{step.agent}",
        )
        record = _execute_record(step, bundle, result, now)
        path = runlog.write(record, dir=runs_dir)
        results.append((step, result, record, path))

    # Save audit log at end of route
    if autonomy_manager:
        summary = autonomy_manager.get_approval_summary()
        autonomy_manager.save_audit_log()
        out(f"Autonomy summary: {summary['auto_approved']} auto-approved, "
            f"{summary['user_approved']} user-approved, {summary['user_rejected']} rejected, "
            f"{summary['blocked']} blocked")

    return results
