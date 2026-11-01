"""Parallel execution of independent lifecycle routes (Phase 2).

Runs several routes concurrently, each in its own git worktree, so two tasks can
make code changes at the same time without colliding in one working tree and
``main`` stays clean. This is the payoff of the Phase 1 worktree isolation: the
driver already isolates a route's builder steps, so N routes in N worktrees are
genuinely independent.

Scope — deliberately narrow:
- The unit of parallelism is a whole **route** (e.g. two separate ``iteration``
  tasks), not agents within one route. Routes are ordered handoff chains by
  design, so intra-route steps stay sequential inside each thread.
- Concurrency is thread-based (``concurrent.futures.ThreadPoolExecutor``): each
  route's work is subprocess-bound I/O (the CLI adapter shells out), so threads
  give real overlap without a process pool, and we stay stdlib-only.

Safety:
- A parallel batch is **refused in ``ask`` autonomy mode** — interleaving
  per-step approval prompts across threads is not something a human can answer
  coherently. Use ``full`` (with ``--yes``) or ``cautious`` (which auto-approves
  LOW/MEDIUM and *declines* anything that would prompt, halting only that route).
- Each thread's ``prompt_fn`` never blocks on stdin: it declines, so a gated step
  stops its own route instead of hanging the whole batch.
- Each route writes run records under its own ``runs_dir`` subdirectory so
  concurrent writers never interleave or clobber each other.

Coordinator discipline holds: this module sequences and isolates; it never
reasons or calls a model. Stdlib only; absolute imports.
"""
from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, List, Optional, Tuple

from scripts.orchestrator import config, driver, sequencer


class ParallelError(Exception):
    """Raised when a parallel batch is misconfigured and refuses to launch."""


@dataclass
class RouteEntry:
    """One route to run, with an optional task tag that namespaces its output."""

    route: str
    tag: str = ""

    @property
    def label(self) -> str:
        """Stable identifier: ``route`` or ``route:tag``."""
        return f"{self.route}:{self.tag}" if self.tag else self.route

    @property
    def runs_subdir(self) -> str:
        """Filesystem-safe per-route subdirectory name for run records."""
        safe = "".join(c if c.isalnum() or c in "-_" else "-" for c in self.label)
        return safe


@dataclass
class RouteOutcome:
    """Result of running one route in the batch."""

    entry: RouteEntry
    status: str  # "completed" | "error"
    results: list = field(default_factory=list)  # execute_route's return value
    error: Optional[str] = None
    step_count: int = 0


def parse_entries(raw_entries: List[str]) -> List[RouteEntry]:
    """Parse ``["iteration:a", "release"]`` into RouteEntry objects.

    A ``route:tag`` splits on the first colon; a bare ``route`` has an empty tag.
    Validates each route name against routing.yaml up front so a typo fails before
    any worktree is created.
    """
    routes = config.load_routing()
    entries: List[RouteEntry] = []
    seen_labels = set()
    for raw in raw_entries:
        raw = raw.strip()
        if not raw:
            continue
        route, _, tag = raw.partition(":")
        route, tag = route.strip(), tag.strip()
        if route not in routes:
            raise ParallelError(
                f"route '{route}' not in routing.yaml (have: {sorted(routes)})"
            )
        entry = RouteEntry(route=route, tag=tag)
        if entry.label in seen_labels:
            raise ParallelError(
                f"duplicate batch entry '{entry.label}' — give each route a "
                f"distinct tag (e.g. {route}:a {route}:b)"
            )
        seen_labels.add(entry.label)
        entries.append(entry)
    if not entries:
        raise ParallelError("no routes given to run")
    return entries


def _decline(*_args, **_kwargs) -> str:
    """A non-interactive prompt: never block a thread on stdin; decline instead."""
    return "n"


def _prefixed_out(label: str, lock: threading.Lock, out: Callable) -> Callable:
    """An ``out`` that tags each line with the route label, atomically."""
    def _emit(msg: str = "") -> None:
        with lock:
            out(f"[{label}] {msg}")
    return _emit


def run_routes(
    raw_entries: List[str],
    adapter_factory: Callable,
    runs_dir: str = "runs",
    max_workers: int = 2,
    assume_yes: bool = False,
    autonomy_mode: Optional[str] = None,
    isolation: Optional[dict] = None,
    out: Callable = print,
    now: Optional[datetime] = None,
) -> List[RouteOutcome]:
    """Run each entry's route concurrently, each isolated in its own worktree.

    Args:
        raw_entries: route specs, each ``route`` or ``route:tag``.
        adapter_factory: zero-arg callable returning a FRESH adapter per route
            (adapters hold no cross-route state, but each thread gets its own to
            avoid any shared mutation).
        runs_dir: base directory for run records; each route writes to a
            ``<runs_dir>/<route:tag>/`` subdirectory.
        max_workers: max routes running at once.
        assume_yes: forwarded to execute_route (skips the per-step checkpoint).
        autonomy_mode: ask|cautious|full. ``ask`` is refused (see module docs).
        isolation: worktree isolation config (forwarded to execute_route so each
            route's builder steps land in that route's own worktree).
        out: output sink (default print).
        now: timestamp override for testing.

    Returns:
        A RouteOutcome per entry, in completion order.

    Raises:
        ParallelError: on ``ask`` mode, bad route names, or an empty batch.
    """
    if autonomy_mode == "ask":
        raise ParallelError(
            "parallel batch cannot run in 'ask' autonomy mode — per-step prompts "
            "across concurrent routes can't be answered coherently. Use --autonomy "
            "full --yes, or --autonomy cautious."
        )

    entries = parse_entries(raw_entries)
    now = now or datetime.now(timezone.utc)
    lock = threading.Lock()

    def _run_one(entry: RouteEntry) -> RouteOutcome:
        route_out = _prefixed_out(entry.label, lock, out)
        route_runs = str(Path(runs_dir) / entry.runs_subdir)
        route_out(f"starting route '{entry.route}' (runs → {route_runs})")
        try:
            results = driver.execute_route(
                entry.route,
                adapter_factory(),
                runs_dir=route_runs,
                assume_yes=assume_yes,
                autonomy_mode=autonomy_mode,
                prompt_fn=_decline,      # never block a thread on stdin
                out=route_out,
                now=now,
                isolation=isolation,
            )
            route_out(f"done — {len(results)} step(s) ran")
            return RouteOutcome(entry=entry, status="completed",
                                results=results, step_count=len(results))
        except Exception as exc:  # one route failing must not sink the batch
            route_out(f"ERROR: {exc}")
            return RouteOutcome(entry=entry, status="error", error=str(exc))

    outcomes: List[RouteOutcome] = []
    workers = max(1, min(max_workers, len(entries)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_run_one, e): e for e in entries}
        for fut in as_completed(futures):
            outcomes.append(fut.result())

    return outcomes


def summarize(outcomes: List[RouteOutcome]) -> Tuple[int, int, int]:
    """Return (completed, errored, total_steps) across the batch."""
    completed = sum(1 for o in outcomes if o.status == "completed")
    errored = sum(1 for o in outcomes if o.status == "error")
    steps = sum(o.step_count for o in outcomes)
    return completed, errored, steps
