import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from scripts.orchestrator import config, evalhook, runlog

_NOW = datetime(2026, 5, 28, 21, 0, 0, tzinfo=timezone.utc)
_ROOT = config.repo_root()
_PLAN_CASE = "evals/cases/planning/basic-feature-plan.md"


class TestResolveRubric(unittest.TestCase):
    def test_from_case_section(self):
        self.assertEqual(
            evalhook.resolve_rubric(_PLAN_CASE), "evals/rubrics/plan-quality.md"
        )

    def test_explicit_override(self):
        self.assertEqual(
            evalhook.resolve_rubric(_PLAN_CASE, explicit="evals/rubrics/agent-output-quality.md"),
            "evals/rubrics/agent-output-quality.md",
        )

    def test_explicit_missing_raises(self):
        with self.assertRaises(evalhook.EvalHookError):
            evalhook.resolve_rubric(_PLAN_CASE, explicit="evals/rubrics/nope.md")

    def test_no_reference_raises(self):
        with tempfile.TemporaryDirectory() as d:
            case = Path(d) / "case.md"
            case.write_text("# Case\n\nNo rubric here.\n", encoding="utf-8")
            with self.assertRaises(evalhook.EvalHookError):
                evalhook.resolve_rubric(str(case))


class TestRubricCriteria(unittest.TestCase):
    def test_plain_bullets(self):
        crits = evalhook.rubric_criteria("evals/rubrics/plan-quality.md")
        self.assertIn("Goal clarity", crits)
        self.assertIn("Handoff clarity", crits)


class TestRunEval(unittest.TestCase):
    def test_scaffolds_stub_and_record(self):
        with tempfile.TemporaryDirectory() as d:
            out = evalhook.run_eval(
                _PLAN_CASE, results_dir=f"{d}/results", runs_dir=f"{d}/runs", now=_NOW
            )
            self.assertEqual(out["rubric"], "evals/rubrics/plan-quality.md")
            stub = Path(out["result"]).read_text(encoding="utf-8")
            self.assertIn("PENDING", stub)
            self.assertIn("Goal clarity", stub)

            parsed = config.load_yaml_string(
                runlog.extract_yaml_block(Path(out["run_record"]).read_text(encoding="utf-8"))
            )
            self.assertEqual(parsed, out["record"].to_dict())
            self.assertEqual(parsed["agent"], "evaluator")
            self.assertEqual(parsed["evaluation"]["rubric"], "evals/rubrics/plan-quality.md")
            self.assertIsNone(parsed["evaluation"]["score"])
            self.assertEqual(parsed["validation"]["status"], "skipped")


class TestCLISmoke(unittest.TestCase):
    def _run(self, *args):
        return subprocess.run(
            [sys.executable, str(_ROOT / "scripts" / "orchestrate.py"), *args],
            capture_output=True, text=True, cwd=str(_ROOT),
        )

    def test_help_lists_subcommands(self):
        result = self._run("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("route", result.stdout)
        self.assertIn("eval", result.stdout)

    def test_route_dry_run_writes_records(self):
        with tempfile.TemporaryDirectory() as d:
            result = self._run("route", "iteration", "--dry-run", "--runs-dir", d)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("planner", result.stdout)
            self.assertEqual(len(list(Path(d).glob("*.md"))), 3)

    def test_eval_resolves_rubric_from_case(self):
        with tempfile.TemporaryDirectory() as d:
            result = self._run("eval", _PLAN_CASE,
                                "--results-dir", f"{d}/res", "--runs-dir", f"{d}/runs")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("plan-quality.md", result.stdout)
            self.assertEqual(len(list((Path(d) / "res").glob("*.md"))), 1)

    def test_unknown_route_errors(self):
        result = self._run("route", "no_such_route")
        self.assertEqual(result.returncode, 2)
        self.assertIn("not in routing.yaml", result.stderr)


if __name__ == "__main__":
    unittest.main()
