import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from scripts.orchestrator import config, driver, runlog
from scripts.orchestrator.adapter import CliAdapter, NoopAdapter

_NOW = datetime(2026, 5, 28, 22, 0, 0, tzinfo=timezone.utc)


def _yes(*_):
    return "y"


def _no(*_):
    return "n"


def _silent(*_args, **_kwargs):
    pass


class TestExecuteRoute(unittest.TestCase):
    def test_noop_executes_all_steps_and_records_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            results = driver.execute_route(
                "iteration", NoopAdapter(), runs_dir=d, assume_yes=True, now=_NOW
            )
            self.assertEqual(len(results), 3)  # planner, builder, evaluator
            for _step, result, record, path in results:
                self.assertEqual(result.status, "skipped")
                self.assertEqual(record.validation["status"], "skipped")
                parsed = config.load_yaml_string(
                    runlog.extract_yaml_block(Path(path).read_text(encoding="utf-8"))
                )
                self.assertEqual(parsed, record.to_dict())

    def test_max_steps_bounds_the_loop(self):
        with tempfile.TemporaryDirectory() as d:
            results = driver.execute_route(
                "iteration", NoopAdapter(), runs_dir=d, max_steps=1, assume_yes=True, now=_NOW
            )
            self.assertEqual(len(results), 1)

    def test_cli_adapter_records_real_outputs(self):
        cmd = [sys.executable, "-c", "import sys; sys.stdout.write('done')"]
        with tempfile.TemporaryDirectory() as d:
            results = driver.execute_route(
                "release", CliAdapter(cmd), runs_dir=d, assume_yes=True, prompt_fn=_yes, now=_NOW
            )
            self.assertEqual(len(results), 1)  # release route = reviewer
            _step, result, record, _path = results[0]
            self.assertEqual(result.status, "executed")
            self.assertEqual(record.validation["status"], "passed")
            self.assertTrue(record.outputs)
            self.assertTrue(any("invoked CLI" in a for a in record.tool_actions))

    def test_cli_adapter_failure_records_high_issue(self):
        cmd = [sys.executable, "-c", "import sys; sys.exit(3)"]
        with tempfile.TemporaryDirectory() as d:
            results = driver.execute_route(
                "release", CliAdapter(cmd), runs_dir=d, assume_yes=True, prompt_fn=_yes, now=_NOW
            )
            _step, result, record, _path = results[0]
            self.assertEqual(result.status, "failed")
            self.assertEqual(record.validation["status"], "failed")
            self.assertTrue(any(i["severity"] == "high" for i in record.issues))

    def test_protected_write_gate_is_not_waived_by_assume_yes(self):
        # tool_integration steps declare an output of configs/tools.yaml (protected).
        with tempfile.TemporaryDirectory() as d:
            results = driver.execute_route(
                "tool_integration", NoopAdapter(), runs_dir=d,
                assume_yes=True, prompt_fn=_no, out=_silent, now=_NOW,
            )
            self.assertEqual(results, [])  # halted at the protected step despite assume_yes

    def test_protected_write_gate_proceeds_when_approved(self):
        with tempfile.TemporaryDirectory() as d:
            results = driver.execute_route(
                "tool_integration", NoopAdapter(), runs_dir=d,
                assume_yes=True, prompt_fn=_yes, now=_NOW,
            )
            self.assertTrue(results)  # approval granted -> runs

    def test_per_step_checkpoint_declined_halts(self):
        with tempfile.TemporaryDirectory() as d:
            results = driver.execute_route(
                "task_definition", NoopAdapter(), runs_dir=d,
                assume_yes=False, prompt_fn=_no, out=_silent, now=_NOW,
            )
            self.assertEqual(results, [])  # declined at first checkpoint


if __name__ == "__main__":
    unittest.main()
