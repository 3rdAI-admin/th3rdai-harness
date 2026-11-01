"""
Unit tests for orchestrator worktree isolation (Phase 1).

Covers the pure, git-free logic of the isolation integration:
- ``_isolation_enabled`` config gating
- ``_worktree_for_step`` graceful degradation (no git side effects)
- ``_classify_step_risk`` honoring the ``isolated`` flag
- per-step ``cwd`` threading through the adapters
- ``execute_route`` backward compatibility (isolation=None) and audit context

Creating real git worktrees is intentionally NOT exercised here: that path is
covered by scripts/worktree.sh's own behavior and by end-to-end runs. These tests
stay hermetic (no worktree dirs to clean up) and fast.
"""
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.orchestrator import driver, sequencer
from scripts.orchestrator.adapter import CliAdapter, NoopAdapter

_NOW = datetime(2026, 5, 28, 22, 0, 0, tzinfo=timezone.utc)


def _silent(*_args, **_kwargs):
    pass


def _yes(*_):
    return "y"


def _builder_step():
    """The builder step from the iteration route (a non-protected write)."""
    steps = sequencer.plan_route("iteration")
    return next(s for s in steps if s.agent == "builder")


class TestIsolationEnabled(unittest.TestCase):
    def test_none_config_disables(self):
        self.assertFalse(driver._isolation_enabled(None, "builder"))

    def test_empty_config_disables(self):
        self.assertFalse(driver._isolation_enabled({}, "builder"))

    def test_enabled_false_disables(self):
        cfg = {"enabled": False, "isolate_agents": ["builder"]}
        self.assertFalse(driver._isolation_enabled(cfg, "builder"))

    def test_agent_not_listed_disables(self):
        cfg = {"enabled": True, "isolate_agents": ["builder"]}
        self.assertFalse(driver._isolation_enabled(cfg, "planner"))

    def test_enabled_and_listed(self):
        cfg = {"enabled": True, "isolate_agents": ["builder"]}
        self.assertTrue(driver._isolation_enabled(cfg, "builder"))

    def test_missing_isolate_agents_disables(self):
        cfg = {"enabled": True}
        self.assertFalse(driver._isolation_enabled(cfg, "builder"))


class TestWorktreeForStepDegradation(unittest.TestCase):
    def test_disabled_returns_none(self):
        """Isolation off for this agent ⇒ run in place (None), no git touched."""
        step = _builder_step()
        self.assertIsNone(
            driver._worktree_for_step(step, None, out=_silent)
        )
        cfg = {"enabled": True, "isolate_agents": ["planner"]}  # not builder
        self.assertIsNone(
            driver._worktree_for_step(step, cfg, out=_silent)
        )


class TestClassifyStepRiskIsolation(unittest.TestCase):
    def _bundle(self):
        return sequencer.build_context(_builder_step())

    def test_isolated_downgrades_ordinary_write(self):
        """Isolation drops an ordinary builder write MEDIUM → LOW."""
        from scripts.orchestrator.autonomy_manager import AutonomyManager
        mgr = AutonomyManager(mode_override="cautious")
        bundle = self._bundle()
        noop = NoopAdapter()
        plain = driver._classify_step_risk(_builder_step(), bundle, noop, mgr,
                                           isolated=False)
        iso = driver._classify_step_risk(_builder_step(), bundle, noop, mgr,
                                         isolated=True)
        self.assertEqual(plain, "MEDIUM")
        self.assertEqual(iso, "LOW")

    def test_no_autonomy_manager_is_medium(self):
        bundle = self._bundle()
        self.assertEqual(
            driver._classify_step_risk(_builder_step(), bundle, NoopAdapter(),
                                       None, isolated=True),
            "MEDIUM",
        )


class TestAdapterCwdThreading(unittest.TestCase):
    def test_cli_adapter_honors_per_call_cwd(self):
        bundle = sequencer.build_context(_builder_step())
        cli = CliAdapter(["python3", "-c", "import os;print(os.getcwd())"],
                         timeout=30)
        with tempfile.TemporaryDirectory() as d:
            # No cwd → repo-root-ish (just assert it is NOT the temp dir).
            r1 = cli.run(bundle, runs_dir=d, label="cwd-none")
            out_none = (Path(d) / "cwd-none-stdout.txt").read_text().strip()
            # Per-call cwd → the temp dir.
            r2 = cli.run(bundle, runs_dir=d, label="cwd-set", cwd=d)
            out_set = (Path(d) / "cwd-set-stdout.txt").read_text().strip()
            self.assertEqual(r1.status, "executed")
            self.assertEqual(r2.status, "executed")
            self.assertNotEqual(out_none, out_set)
            # Resolve both sides: macOS reports /private/var for /var tmp dirs.
            self.assertEqual(Path(out_set).resolve(), Path(d).resolve())

    def test_noop_adapter_accepts_cwd(self):
        """NoopAdapter.run tolerates cwd (signature parity) and notes it."""
        bundle = sequencer.build_context(_builder_step())
        res = NoopAdapter().run(bundle, cwd="/tmp/some-worktree")
        self.assertEqual(res.status, "skipped")
        self.assertIn("/tmp/some-worktree", res.notes)


class TestExecuteRouteBackwardCompat(unittest.TestCase):
    def test_isolation_none_runs_in_place_and_records_not_isolated(self):
        """Default (isolation=None) is unchanged behavior; audit shows isolated=False."""
        with tempfile.TemporaryDirectory() as d:
            results = driver.execute_route(
                "iteration", NoopAdapter(), runs_dir=d,
                assume_yes=True, autonomy_mode="full",
                prompt_fn=_yes, out=_silent, now=_NOW, isolation=None,
            )
            self.assertEqual(len(results), 3)  # planner, builder, evaluator
            for _step, result, _record, _path in results:
                self.assertEqual(result.status, "skipped")

    def test_isolation_for_unmatched_agent_is_in_place(self):
        """Config enabled but only for an agent not in this route ⇒ no isolation."""
        with tempfile.TemporaryDirectory() as d:
            cfg = {"enabled": True, "isolate_agents": ["nonexistent-agent"]}
            results = driver.execute_route(
                "iteration", NoopAdapter(), runs_dir=d,
                assume_yes=True, autonomy_mode="full",
                prompt_fn=_yes, out=_silent, now=_NOW, isolation=cfg,
            )
            self.assertEqual(len(results), 3)


if __name__ == "__main__":
    unittest.main()
