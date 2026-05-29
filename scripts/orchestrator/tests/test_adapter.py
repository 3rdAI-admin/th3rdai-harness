"""Tests for the execution adapters (NoopAdapter / CliAdapter + StepResult).

Uses a tiny fake bundle (no sequencer import) and a tmp ``runs_dir`` so nothing
touches the real repo or invokes a model beyond a trivial stubbed python CLI.
"""
import os
import sys
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path

from scripts.orchestrator import adapter
from scripts.orchestrator.adapter import AdapterError, CliAdapter, NoopAdapter


@dataclass
class _FakeStep:
    route: str = "r"
    order: int = 1
    agent: str = "planner"


class _FakeBundle:
    """Opaque-enough stand-in: only .render(), .outputs, .step are used."""

    def __init__(self):
        self.step = _FakeStep()
        self.outputs = ["output/x.md"]

    def render(self) -> str:
        return "RENDERED BUNDLE TEXT"


class TestNoopAdapter(unittest.TestCase):
    def test_skips_without_writing_files(self):
        bundle = _FakeBundle()
        with tempfile.TemporaryDirectory() as d:
            result = NoopAdapter().run(bundle, runs_dir=d)
            self.assertEqual(result.status, "skipped")
            self.assertEqual(result.outputs, bundle.outputs)
            self.assertIsNone(result.exit_code)
            self.assertEqual(os.listdir(d), [], "noop must not write files")

    def test_name(self):
        self.assertEqual(NoopAdapter().name, "noop")


class TestCliAdapterSuccess(unittest.TestCase):
    def test_executed_writes_stdout(self):
        bundle = _FakeBundle()
        cmd = [sys.executable, "-c", "import sys; sys.stdout.write('hello')"]
        with tempfile.TemporaryDirectory() as d:
            result = CliAdapter(cmd).run(bundle, runs_dir=d)
            self.assertEqual(result.status, "executed")
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.name if hasattr(result, "name") else CliAdapter(cmd).name, "cli")
            self.assertTrue(result.stdout_path)
            self.assertEqual(len(result.outputs), 1)
            # Path is outside the repo (tmp dir) -> stored as-is and exists.
            stdout_file = Path(result.stdout_path)
            self.assertTrue(stdout_file.exists())
            self.assertEqual(stdout_file.read_text(encoding="utf-8"), "hello")


class TestCliAdapterFailure(unittest.TestCase):
    def test_nonzero_exit_is_failed(self):
        bundle = _FakeBundle()
        cmd = [sys.executable, "-c", "import sys; sys.exit(3)"]
        with tempfile.TemporaryDirectory() as d:
            result = CliAdapter(cmd).run(bundle, runs_dir=d)
            self.assertEqual(result.status, "failed")
            self.assertEqual(result.exit_code, 3)


class TestCliAdapterMisconfigured(unittest.TestCase):
    def test_empty_command_raises(self):
        with self.assertRaises(AdapterError):
            CliAdapter([]).run(_FakeBundle(), runs_dir="runs")


class TestCliAdapterTimeout(unittest.TestCase):
    def test_timeout_is_failed_with_note(self):
        bundle = _FakeBundle()
        cmd = [sys.executable, "-c", "import time; time.sleep(2)"]
        with tempfile.TemporaryDirectory() as d:
            result = CliAdapter(cmd, timeout=0.2).run(bundle, runs_dir=d)
            self.assertEqual(result.status, "failed")
            self.assertIsNone(result.exit_code)
            self.assertIn("timeout", result.notes.lower())


class TestScrubbedEnv(unittest.TestCase):
    def test_env_is_minimal_allowlist(self):
        env = CliAdapter._scrubbed_env()
        self.assertEqual(set(env), {"PATH", "HOME", "LANG"})


if __name__ == "__main__":
    unittest.main()
