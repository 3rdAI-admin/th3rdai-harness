"""Execution adapters: turn a sequencer context bundle into a real (or dry-run) step.

This is the opt-in, approval-gated execution layer described in
``plans/native-orchestrator/04-execution-adapter.md``. An :class:`Adapter`
takes an opaque context bundle (Phase 02 ``sequencer.ContextBundle``) and runs
the step, returning a :class:`StepResult`. The bundle is treated as opaque
except for ``.render() -> str`` (the prompt text), ``.outputs`` (declared output
paths), and ``.step`` (``.route`` / ``.order`` / ``.agent`` for naming).

Two adapters ship here:

- :class:`NoopAdapter` preserves today's dry-run semantics: no subprocess, no
  files written, ``status="skipped"``. This is the safe default.
- :class:`CliAdapter` shells out (stdlib :mod:`subprocess`) to an
  already-installed agent CLI, feeding the rendered bundle on stdin and
  capturing stdout/stderr to files under ``runs/``.

Safety model (per the plan's Safety/Tooling Notes):

- **Scrubbed env.** The subprocess never inherits the full ``os.environ`` (which
  may hold API keys or other secrets). It receives a minimal base allowlist
  (``PATH``/``HOME``/``LANG``/``USER``) plus optional names from
  ``configs/execution.yaml`` ``cli.env_allowlist`` when a CLI needs specific
  credential variables.
- **Capture under runs/.** stdout/stderr are written beneath the run directory;
  persisted paths are repo-relative when inside the repo so no absolute,
  machine-specific paths leak into run records.
- **Fail loudly.** A :class:`CliAdapter` with no command refuses to run
  (:class:`AdapterError`); it never silently falls back to a different behavior.

Stdlib only; no pip dependencies. Run from the repo root with absolute imports.
"""
from __future__ import annotations

import os
import subprocess
import typing
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from scripts.orchestrator import config


@dataclass
class StepResult:
    """Outcome of executing (or skipping) a single sequencer step.

    ``status`` is one of ``"skipped"`` (dry run, no model invoked),
    ``"executed"`` (CLI ran and exited 0), or ``"failed"`` (CLI exited non-zero
    or timed out). Path fields are repo-relative when the file lives inside the
    repo, otherwise stored as-is.
    """

    status: str
    outputs: List[str] = field(default_factory=list)
    tool_actions: List[str] = field(default_factory=list)
    exit_code: Optional[int] = None
    stdout_path: Optional[str] = None
    stderr_path: Optional[str] = None
    notes: str = ""


class AdapterError(Exception):
    """Raised when an adapter is misconfigured and refuses to run."""


@typing.runtime_checkable
class Adapter(typing.Protocol):
    """Protocol every execution adapter satisfies."""

    name: str

    def run(self, bundle, runs_dir: str = "runs",
            label: Optional[str] = None) -> StepResult:
        ...


def _resolve_runs_dir(runs_dir: str) -> Path:
    """Resolve ``runs_dir`` to an absolute Path (relative -> under repo root)."""
    p = Path(runs_dir)
    if not p.is_absolute():
        p = config.repo_root() / p
    p.mkdir(parents=True, exist_ok=True)
    return p


def _portable(path: Path) -> str:
    """Repo-relative string when ``path`` is under the repo root, else absolute.

    Keeps run records free of absolute, machine-specific paths whenever the
    capture file lives inside the repo (tests use a tmp dir outside it, which is
    fine — we just return the absolute path in that case).
    """
    try:
        return str(path.relative_to(config.repo_root()))
    except ValueError:
        return str(path)


class NoopAdapter:
    """Dry-run adapter: assembles context but invokes no model and writes no files."""

    name = "noop"

    def run(self, bundle, runs_dir: str = "runs",
            label: Optional[str] = None) -> StepResult:
        return StepResult(
            status="skipped",
            outputs=list(getattr(bundle, "outputs", []) or []),
            tool_actions=["assembled context bundle (dry run; no model invoked)"],
            notes="dry run; no model invoked",
        )


class CliAdapter:
    """Execute a step by shelling out to a configured agent CLI.

    ``command`` is a list[str] (e.g. ``["claude", "-p"]`` or
    ``["python3", "-c", "..."]``). The rendered bundle is fed on stdin; stdout
    and stderr are captured to files under ``runs_dir``. The subprocess runs
    with a scrubbed environment to avoid leaking secrets.
    """

    name = "cli"

    _BASE_ENV_KEYS = ("PATH", "HOME", "LANG", "USER")

    def __init__(self, command, timeout: float = 120.0,
                 cwd: Optional[str] = None,
                 env_allowlist: Optional[List[str]] = None):
        self.command = list(command) if command else []
        self.timeout = timeout
        self.cwd = cwd
        self.env_allowlist = list(env_allowlist) if env_allowlist else []

    @classmethod
    def _scrubbed_env(cls, extra_keys: Optional[List[str]] = None) -> dict:
        """Minimal env for the subprocess plus optional configured passthrough keys.

        Deliberately NOT the full ``os.environ``. Base keys let the CLI resolve
        itself and read credentials under ``HOME`` (e.g. Claude Code login).
        ``extra_keys`` copies only named variables that exist in the parent env.
        """
        env = {k: os.environ.get(k, "") for k in cls._BASE_ENV_KEYS}
        for key in extra_keys or []:
            if key in os.environ:
                env[key] = os.environ[key]
        return env

    def run(self, bundle, runs_dir: str = "runs",
            label: Optional[str] = None) -> StepResult:
        if not self.command:
            raise AdapterError("no CLI command configured")

        step = bundle.step
        label = label or f"{step.route}-{step.order:02d}-{step.agent}"

        runs_path = _resolve_runs_dir(runs_dir)
        stdout_file = runs_path / f"{label}-stdout.txt"
        stderr_file = runs_path / f"{label}-stderr.txt"

        program = self.command[0]
        tool_actions = [f"invoked CLI: {program}"]

        try:
            proc = subprocess.run(
                self.command,
                input=bundle.render(),
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=self.cwd,
                env=self._scrubbed_env(self.env_allowlist),
            )
        except subprocess.TimeoutExpired:
            return StepResult(
                status="failed",
                outputs=[],
                tool_actions=tool_actions,
                exit_code=None,
                notes=f"timeout after {self.timeout}s",
            )

        stdout_file.write_text(proc.stdout or "", encoding="utf-8")
        stderr_file.write_text(proc.stderr or "", encoding="utf-8")

        stdout_rel = _portable(stdout_file)
        stderr_rel = _portable(stderr_file)
        status = "executed" if proc.returncode == 0 else "failed"
        notes = (
            f"CLI '{program}' exited {proc.returncode} ({status})"
        )

        return StepResult(
            status=status,
            outputs=[stdout_rel],
            tool_actions=tool_actions,
            exit_code=proc.returncode,
            stdout_path=stdout_rel,
            stderr_path=stderr_rel,
            notes=notes,
        )
