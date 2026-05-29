"""Run-record writer: emits Markdown-wrapped YAML per telemetry/run-log-schema.md.

The writer renders only the YAML subset that ``orchestrator.config`` can read back,
so every record round-trips (write -> extract block -> ``config.load_yaml_string``).
Scalars stay single-line; no folded/literal block scalars are emitted.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from orchestrator import config

_YAML_BLOCK = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
_SLUG = re.compile(r"[^a-z0-9]+")
_RESERVED = {"null", "Null", "NULL", "~", "true", "True", "TRUE",
             "false", "False", "FALSE", "[]", "{}", ""}


def new_run_id(short_name: str, now: Optional[datetime] = None) -> str:
    now = now or datetime.now(timezone.utc)
    slug = _SLUG.sub("-", short_name.lower()).strip("-") or "run"
    return f"{now:%Y%m%d-%H%M%S}-{slug}"


@dataclass
class RunRecord:
    run_id: str
    created_at: str
    request: str
    agent: str
    skill: Optional[str] = None
    prompt_version: Optional[str] = None
    model_profile: Optional[str] = None
    inputs: list = field(default_factory=list)
    outputs: list = field(default_factory=list)
    tool_actions: list = field(default_factory=list)
    validation: dict = field(default_factory=lambda: {"status": "skipped", "notes": ""})
    evaluation: Optional[dict] = None
    issues: list = field(default_factory=list)
    follow_up: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "created_at": self.created_at,
            "request": self.request,
            "agent": self.agent,
            "skill": self.skill,
            "prompt_version": self.prompt_version,
            "model_profile": self.model_profile,
            "inputs": list(self.inputs),
            "outputs": list(self.outputs),
            "tool_actions": list(self.tool_actions),
            "validation": {
                "status": self.validation.get("status"),
                "notes": self.validation.get("notes", ""),
            },
            "evaluation": (None if self.evaluation is None else {
                "rubric": self.evaluation.get("rubric"),
                "score": self.evaluation.get("score"),
                "notes": self.evaluation.get("notes", ""),
            }),
            "issues": [
                {"severity": i.get("severity"), "description": i.get("description")}
                for i in self.issues
            ],
            "follow_up": list(self.follow_up),
        }


def _needs_quotes(s: str) -> bool:
    if s != s.strip() or s in _RESERVED:
        return True
    if s[0] in "-?:,[]{}#&*!|>'\"%@`":
        return True
    if ": " in s or s.endswith(":") or " #" in s:
        return True
    try:
        float(s)
        return True
    except ValueError:
        return False


def _dump_scalar(value) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, float):
        return repr(value)
    if isinstance(value, int):
        return str(value)
    s = str(value)
    if "\n" in s:
        raise ValueError("run-record scalars must be single-line (no newlines)")
    if _needs_quotes(s):
        quote = '"' if "'" in s else "'"
        return f"{quote}{s}{quote}"
    return s


def _dump_str_list(lines, key, items):
    if not items:
        lines.append(f"{key}: []")
        return
    lines.append(f"{key}:")
    for item in items:
        lines.append(f"  - {_dump_scalar(item)}")


def render(record: RunRecord) -> str:
    d = record.to_dict()
    lines = []
    for key in ("run_id", "created_at", "request", "agent",
                "skill", "prompt_version", "model_profile"):
        lines.append(f"{key}: {_dump_scalar(d[key])}")
    for key in ("inputs", "outputs", "tool_actions"):
        _dump_str_list(lines, key, d[key])

    val = d["validation"]
    lines.append("validation:")
    lines.append(f"  status: {_dump_scalar(val['status'])}")
    lines.append(f"  notes: {_dump_scalar(val['notes'])}")

    ev = d["evaluation"]
    if ev is None:
        lines.append("evaluation: null")
    else:
        lines.append("evaluation:")
        lines.append(f"  rubric: {_dump_scalar(ev['rubric'])}")
        lines.append(f"  score: {_dump_scalar(ev['score'])}")
        lines.append(f"  notes: {_dump_scalar(ev['notes'])}")

    if not d["issues"]:
        lines.append("issues: []")
    else:
        lines.append("issues:")
        for issue in d["issues"]:
            lines.append(f"  - severity: {_dump_scalar(issue['severity'])}")
            lines.append(f"    description: {_dump_scalar(issue['description'])}")

    _dump_str_list(lines, "follow_up", d["follow_up"])
    return "\n".join(lines) + "\n"


def write(record: RunRecord, dir: str = "runs", title: Optional[str] = None) -> Path:
    out_dir = Path(dir)
    if not out_dir.is_absolute():
        out_dir = config.repo_root() / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    heading = title or record.request or record.run_id
    body = (
        f"# Run: {heading}\n\n"
        "Generated by the native orchestrator. Conforms to `telemetry/run-log-schema.md`.\n\n"
        f"```yaml\n{render(record)}```\n"
    )
    path = out_dir / f"{record.run_id}.md"
    path.write_text(body, encoding="utf-8")
    return path


def extract_yaml_block(markdown: str) -> str:
    match = _YAML_BLOCK.search(markdown)
    if not match:
        raise ValueError("no ```yaml block found in run record")
    return match.group(1)
