"""Stage/agent sequencer (dry-run): turn a lifecycle route into ordered steps and
assemble a per-step context bundle, without invoking any model.

Field sources for a context bundle (see plans/native-orchestrator/02-sequencer.md):
  - contract + default_skill + model_profile : ``configs/agents.yaml``
  - prompt version  : ``prompts/registry.md`` (Current Version keyed by Agent),
                      fallback latest ``prompts/<agent>/vN.md``, else None
  - model settings  : ``configs/models.yaml`` (by profile name)
  - declared inputs/outputs : the step's stage contract ``stages/NN/CONTEXT.md``
                      (``## Inputs`` File column, ``## Outputs`` Location column)

Coordinator only: this never reasons or calls an LLM. Dry-run writes a run record
per step with ``validation.status: skipped``.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from scripts.orchestrator import config, runlog

_VERSION_FILE = re.compile(r"v(\d+)\.md$")


class SequencerError(ValueError):
    """Raised when a route or its referenced agents cannot be resolved."""


@dataclass
class Step:
    route: str
    stage: Optional[str]
    agent: str
    order: int
    contract: Optional[str] = None
    default_skill: Optional[str] = None
    model_profile: Optional[str] = None


@dataclass
class ContextBundle:
    step: Step
    contract: Optional[str] = None
    skill: Optional[str] = None
    prompt_version: Optional[str] = None
    model_profile: Optional[str] = None
    model_settings: Optional[dict] = None
    stage_contract: Optional[str] = None
    inputs: list = field(default_factory=list)
    outputs: list = field(default_factory=list)
    missing: list = field(default_factory=list)

    def render(self) -> str:
        s = self.step
        lines = [
            f"Step {s.order}: {s.agent} @ {s.stage or '(no stage)'} [route: {s.route}]",
            f"  contract      : {self.contract or 'null'}",
            f"  skill         : {self.skill or 'null'}",
            f"  prompt        : {self.prompt_version or 'null'}",
            f"  model_profile : {self.model_profile or 'null'}",
            f"  stage_contract: {self.stage_contract or 'null'}",
            f"  inputs        : {', '.join(self.inputs) if self.inputs else '(none declared)'}",
            f"  outputs       : {', '.join(self.outputs) if self.outputs else '(none declared)'}",
        ]
        if self.missing:
            lines.append(f"  MISSING REFS  : {', '.join(self.missing)}")
        return "\n".join(lines)


# --- markdown table helpers (stage contracts + prompt registry) -------------

def _is_table_row(line: str) -> bool:
    s = line.strip()
    return len(s) >= 2 and s.startswith("|") and s.endswith("|")


def _cells(line: str) -> list:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _is_separator_row(line: str) -> bool:
    return all(c and set(c) <= set("-: ") for c in _cells(line))


def _strip_ticks(s: str) -> str:
    return s.replace("`", "").strip()


def _read_table(lines: list, start: int = 0):
    """Return (header_cells, data_rows) for the first markdown table at/after start."""
    i = start
    while i < len(lines) and not _is_table_row(lines[i]):
        i += 1
    if i >= len(lines):
        return None, []
    header = _cells(lines[i])
    i += 1
    if i < len(lines) and _is_separator_row(lines[i]):
        i += 1
    rows = []
    while i < len(lines) and _is_table_row(lines[i]):
        rows.append(_cells(lines[i]))
        i += 1
    return header, rows


def _section_lines(md_text: str, heading: str) -> list:
    target = f"## {heading}".lower()
    out, capturing = [], False
    for line in md_text.splitlines():
        if line.strip().lower().startswith("## "):
            if capturing:
                break
            capturing = line.strip().lower() == target
            continue
        if capturing:
            out.append(line)
    return out


def _column(header, rows, name, fallback_idx=0) -> list:
    idx = fallback_idx
    if header:
        for i, h in enumerate(header):
            if h.strip().lower() == name.lower():
                idx = i
                break
    out = []
    for row in rows:
        if idx < len(row):
            value = _strip_ticks(row[idx])
            if value:
                out.append(value)
    return out


def _stage_io(md_text: str):
    in_header, in_rows = _read_table(_section_lines(md_text, "Inputs"))
    out_header, out_rows = _read_table(_section_lines(md_text, "Outputs"))
    inputs = _column(in_header, in_rows, "File", 0)
    outputs = _column(out_header, out_rows, "Location", 1)
    return inputs, outputs


# --- prompt resolution ------------------------------------------------------

def resolve_prompt(agent_name: str) -> Optional[str]:
    """Repo-relative prompt path for an agent, or None.

    Primary source is ``prompts/registry.md`` (Current Version keyed by Agent);
    falls back to the highest-numbered ``prompts/<agent>/vN.md`` on disk.
    """
    root = config.repo_root()
    registry = root / "prompts" / "registry.md"
    if registry.exists():
        header, rows = _read_table(registry.read_text(encoding="utf-8").splitlines())
        if header:
            cols = {h.strip().lower(): i for i, h in enumerate(header)}
            ai, vi = cols.get("agent"), cols.get("current version")
            if ai is not None and vi is not None:
                for row in rows:
                    if ai < len(row) and row[ai].strip().lower() == agent_name.lower():
                        version = _strip_ticks(row[vi]) if vi < len(row) else ""
                        candidate = f"prompts/{version}" if version else None
                        if candidate and (root / candidate).exists():
                            return candidate
                        break  # named in registry but missing -> try convention
    prompt_dir = root / "prompts" / agent_name
    if prompt_dir.is_dir():
        versions = []
        for path in prompt_dir.glob("v*.md"):
            match = _VERSION_FILE.search(path.name)
            if match:
                versions.append((int(match.group(1)), path.name))
        if versions:
            versions.sort()
            return f"prompts/{agent_name}/{versions[-1][1]}"
    return None


# --- planning + context assembly --------------------------------------------

def plan_route(route_name: str) -> list:
    routes = config.load_routing()
    agents = config.load_agents()
    if route_name not in routes:
        raise SequencerError(
            f"route '{route_name}' not in routing.yaml (have: {sorted(routes)})"
        )
    spec = routes[route_name]
    stage = spec.get("stage")
    steps = []
    for order, agent_name in enumerate(spec.get("agents", []) or [], start=1):
        if agent_name not in agents:
            raise SequencerError(
                f"route '{route_name}': agent '{agent_name}' not defined in agents.yaml"
            )
        a = agents[agent_name]
        steps.append(Step(
            route=route_name,
            stage=stage,
            agent=agent_name,
            order=order,
            contract=a.get("contract"),
            default_skill=a.get("default_skill"),
            model_profile=a.get("model_profile"),
        ))
    return steps


def build_context(step: Step) -> ContextBundle:
    root = config.repo_root()
    missing = []

    def track(rel):
        if rel and not (root / rel).exists():
            missing.append(rel)
        return rel

    contract = track(step.contract)
    skill = track(step.default_skill) if step.default_skill else None
    prompt_version = resolve_prompt(step.agent)
    if prompt_version:
        track(prompt_version)

    model_settings = None
    if step.model_profile:
        models = config.load_models()
        model_settings = models.get(step.model_profile)
        if model_settings is None:
            missing.append(f"model_profile:{step.model_profile}")

    stage_contract = f"{step.stage}/CONTEXT.md" if step.stage else None
    inputs, outputs = [], []
    if stage_contract:
        if (root / stage_contract).exists():
            inputs, outputs = _stage_io((root / stage_contract).read_text(encoding="utf-8"))
        else:
            missing.append(stage_contract)

    return ContextBundle(
        step=step,
        contract=contract,
        skill=skill,
        prompt_version=prompt_version,
        model_profile=step.model_profile,
        model_settings=model_settings,
        stage_contract=stage_contract,
        inputs=inputs,
        outputs=outputs,
        missing=missing,
    )


def _bundle_to_record(bundle: ContextBundle, now: datetime) -> runlog.RunRecord:
    step = bundle.step
    run_id = runlog.new_run_id(f"{step.route}-{step.order:02d}-{step.agent}", now=now)
    notes = "dry run; coordinator assembled context bundle, did not invoke a model"
    if bundle.missing:
        notes += f"; missing refs: {', '.join(bundle.missing)}"

    inputs = [p for p in (bundle.contract, bundle.skill, bundle.prompt_version,
                          bundle.stage_contract) if p]
    inputs.extend(bundle.inputs)

    issues = [
        {"severity": "medium", "description": f"missing referenced file: {m}"}
        for m in bundle.missing
    ]
    return runlog.RunRecord(
        run_id=run_id,
        created_at=now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        request=f"Dry-run step {step.order} of route '{step.route}': {step.agent} @ {step.stage}",
        agent=step.agent,
        skill=step.default_skill,
        prompt_version=bundle.prompt_version,
        model_profile=step.model_profile,
        inputs=inputs,
        outputs=list(bundle.outputs),
        tool_actions=[
            "resolved route step from configs",
            "assembled context bundle (dry run; no model invoked)",
        ],
        validation={"status": "skipped", "notes": notes},
        issues=issues,
        follow_up=["execute step via the Phase 04 adapter when --execute is enabled"],
    )


def dry_run(route_name: str, runs_dir: str = "runs",
            now: Optional[datetime] = None, write_records: bool = True) -> list:
    """Plan a route, assemble each step's bundle, and (optionally) write a dry-run
    run record per step. Returns a list of (bundle, record, path)."""
    now = now or datetime.now(timezone.utc)
    results = []
    for step in plan_route(route_name):
        bundle = build_context(step)
        record = _bundle_to_record(bundle, now)
        path = runlog.write(record, dir=runs_dir) if write_records else None
        results.append((bundle, record, path))
    return results
