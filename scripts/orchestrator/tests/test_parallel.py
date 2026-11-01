"""
Unit tests for parallel route execution (Phase 2).

Hermetic: uses NoopAdapter with isolation=None (no real git worktrees, nothing to
clean up). Covers entry parsing/validation, the ask-mode refusal, duplicate
detection, concurrent execution, per-route run-record namespacing, and fault
isolation (one route failing must not sink the batch).
"""
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.orchestrator import parallel
from scripts.orchestrator.adapter import NoopAdapter

_NOW = datetime(2026, 5, 28, 22, 0, 0, tzinfo=timezone.utc)


def _silent(*_a, **_k):
    pass


class TestParseEntries(unittest.TestCase):
    def test_bare_route(self):
        entries = parallel.parse_entries(["iteration"])
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].route, "iteration")
        self.assertEqual(entries[0].tag, "")
        self.assertEqual(entries[0].label, "iteration")

    def test_route_with_tag(self):
        (e,) = parallel.parse_entries(["iteration:taskA"])
        self.assertEqual(e.route, "iteration")
        self.assertEqual(e.tag, "taskA")
        self.assertEqual(e.label, "iteration:taskA")

    def test_runs_subdir_is_filesystem_safe(self):
        (e,) = parallel.parse_entries(["iteration:task/A"])
        self.assertNotIn(":", e.runs_subdir)
        self.assertNotIn("/", e.runs_subdir)

    def test_unknown_route_rejected(self):
        with self.assertRaises(parallel.ParallelError):
            parallel.parse_entries(["does-not-exist"])

    def test_duplicate_label_rejected(self):
        with self.assertRaises(parallel.ParallelError):
            parallel.parse_entries(["iteration", "iteration"])

    def test_same_route_distinct_tags_ok(self):
        entries = parallel.parse_entries(["iteration:a", "iteration:b"])
        self.assertEqual([e.label for e in entries], ["iteration:a", "iteration:b"])

    def test_empty_rejected(self):
        with self.assertRaises(parallel.ParallelError):
            parallel.parse_entries(["", "  "])


class TestRunRoutes(unittest.TestCase):
    def test_ask_mode_is_refused(self):
        with self.assertRaises(parallel.ParallelError):
            parallel.run_routes(
                ["iteration:a", "iteration:b"],
                adapter_factory=NoopAdapter,
                autonomy_mode="ask",
                out=_silent,
            )

    def test_two_routes_run_and_namespace_records(self):
        with tempfile.TemporaryDirectory() as d:
            outcomes = parallel.run_routes(
                ["task_definition:a", "task_definition:b"],
                adapter_factory=NoopAdapter,
                runs_dir=d,
                autonomy_mode="full",
                assume_yes=True,
                isolation=None,
                out=_silent,
                now=_NOW,
                max_workers=2,
            )
            self.assertEqual(len(outcomes), 2)
            self.assertTrue(all(o.status == "completed" for o in outcomes))
            # Each route wrote to its own subdirectory.
            subdirs = {o.entry.runs_subdir for o in outcomes}
            for sub in subdirs:
                self.assertTrue((Path(d) / sub).is_dir(),
                                f"missing run subdir {sub}")
            completed, errored, steps = parallel.summarize(outcomes)
            self.assertEqual((completed, errored), (2, 0))
            self.assertEqual(steps, 4)  # 2 routes x 2 steps (researcher, planner)

    def test_one_route_error_does_not_sink_batch(self):
        """A route that raises is recorded as errored; others still complete."""
        class _BoomAdapter:
            name = "boom"
            def run(self, *a, **k):
                raise RuntimeError("boom")

        calls = {"n": 0}

        def _factory():
            # First route gets the exploding adapter, the rest get noop.
            calls["n"] += 1
            return _BoomAdapter() if calls["n"] == 1 else NoopAdapter()

        with tempfile.TemporaryDirectory() as d:
            outcomes = parallel.run_routes(
                ["task_definition:boom", "task_definition:ok"],
                adapter_factory=_factory,
                runs_dir=d,
                autonomy_mode="full",
                assume_yes=True,
                isolation=None,
                out=_silent,
                now=_NOW,
                max_workers=1,  # deterministic: boom first
            )
            statuses = {o.entry.label: o.status for o in outcomes}
            self.assertEqual(statuses["task_definition:boom"], "error")
            self.assertEqual(statuses["task_definition:ok"], "completed")
            completed, errored, _ = parallel.summarize(outcomes)
            self.assertEqual((completed, errored), (1, 1))

    def test_empty_batch_raises(self):
        with self.assertRaises(parallel.ParallelError):
            parallel.run_routes([], adapter_factory=NoopAdapter, out=_silent)


if __name__ == "__main__":
    unittest.main()
