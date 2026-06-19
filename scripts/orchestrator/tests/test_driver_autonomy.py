"""
Integration tests for driver.py autonomy integration

Tests the 3-mode autonomy system integrated with execute_route(), including:
- Mode-specific approval behavior
- Audit log creation
- Backward compatibility (no autonomy.yaml)
- Summary reporting

Part of v1.2.0 3-Mode Autonomy System
"""

import unittest
import tempfile
import json
from pathlib import Path
from datetime import datetime, timezone
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.orchestrator import driver, adapter, sequencer, config


class TestDriverAutonomy(unittest.TestCase):
    """Test driver.py autonomy integration"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_runs_dir = tempfile.mkdtemp()
        self.now = datetime(2026, 6, 19, 12, 0, 0, tzinfo=timezone.utc)

    def tearDown(self):
        """Clean up test artifacts"""
        # Clean up temp runs dir
        import shutil
        shutil.rmtree(self.test_runs_dir, ignore_errors=True)

    def test_cautious_mode_auto_approves_medium(self):
        """Cautious mode auto-approves MEDIUM risk operations."""
        # Create a noop adapter
        test_adapter = adapter.NoopAdapter()

        # Execute with cautious mode (no prompts, assume_yes)
        results = driver.execute_route(
            "release",  # Single-step route
            test_adapter,
            runs_dir=self.test_runs_dir,
            autonomy_mode="cautious",
            assume_yes=True,
            now=self.now
        )

        # Should complete 1 step
        self.assertEqual(len(results), 1)
        step, result, record, path = results[0]
        self.assertEqual(result.status, "skipped")  # NoopAdapter skips

    def test_full_mode_auto_approves_all(self):
        """Full mode auto-approves all risk levels."""
        test_adapter = adapter.NoopAdapter()

        results = driver.execute_route(
            "iteration",  # Multi-step route
            test_adapter,
            runs_dir=self.test_runs_dir,
            max_steps=2,
            autonomy_mode="full",
            assume_yes=True,
            now=self.now
        )

        # Should complete 2 steps
        self.assertEqual(len(results), 2)

    def test_audit_log_created(self):
        """Audit log is created when autonomy is enabled."""
        test_adapter = adapter.NoopAdapter()

        # Ensure clean audit log
        audit_path = Path("runs/autonomy-decisions.jsonl")
        if audit_path.exists():
            audit_path.unlink()

        results = driver.execute_route(
            "release",
            test_adapter,
            runs_dir=self.test_runs_dir,
            autonomy_mode="cautious",
            assume_yes=True,
            now=self.now
        )

        # Audit log should exist
        self.assertTrue(audit_path.exists())

        # Should have entries
        with open(audit_path, 'r') as f:
            entries = [json.loads(line) for line in f]

        self.assertGreater(len(entries), 0)

        # Verify entry structure
        entry = entries[0]
        self.assertIn("timestamp", entry)
        self.assertIn("mode", entry)
        self.assertIn("operation", entry)
        self.assertIn("risk_level", entry)
        self.assertIn("decision", entry)
        self.assertEqual(entry["mode"], "cautious")

    def test_backward_compatibility_no_config(self):
        """Execution works without autonomy.yaml (backward compat)."""
        # Temporarily rename autonomy.yaml
        autonomy_path = config.repo_root() / "configs" / "autonomy.yaml"
        backup_path = autonomy_path.parent / "autonomy.yaml.test_backup"

        had_config = autonomy_path.exists()
        if had_config:
            autonomy_path.rename(backup_path)

        try:
            test_adapter = adapter.NoopAdapter()

            # Should work without autonomy config (fall back to legacy gates)
            results = driver.execute_route(
                "release",
                test_adapter,
                runs_dir=self.test_runs_dir,
                assume_yes=True,
                now=self.now
            )

            # Should complete successfully
            self.assertEqual(len(results), 1)

        finally:
            # Restore autonomy.yaml
            if had_config and backup_path.exists():
                backup_path.rename(autonomy_path)

    def test_ask_mode_with_auto_approval(self):
        """Ask mode prompts can be auto-answered with mock prompt function."""
        test_adapter = adapter.NoopAdapter()

        # Mock prompt that auto-approves
        def auto_approve(msg):
            return "y"

        results = driver.execute_route(
            "release",
            test_adapter,
            runs_dir=self.test_runs_dir,
            autonomy_mode="ask",
            prompt_fn=auto_approve,
            now=self.now
        )

        # Should complete with approval
        self.assertEqual(len(results), 1)

    def test_ask_mode_with_rejection(self):
        """Ask mode rejection halts execution."""
        test_adapter = adapter.NoopAdapter()

        # Mock prompt that rejects
        def reject(msg):
            return "n"

        results = driver.execute_route(
            "iteration",
            test_adapter,
            runs_dir=self.test_runs_dir,
            max_steps=2,
            autonomy_mode="ask",
            prompt_fn=reject,
            now=self.now
        )

        # Should halt at first step
        self.assertEqual(len(results), 0)

    def test_mode_override_supersedes_config(self):
        """CLI mode override supersedes config default."""
        test_adapter = adapter.NoopAdapter()

        # Ensure clean audit log
        audit_path = Path("runs/autonomy-decisions.jsonl")
        if audit_path.exists():
            audit_path.unlink()

        # Run with full mode override
        results = driver.execute_route(
            "release",
            test_adapter,
            runs_dir=self.test_runs_dir,
            autonomy_mode="full",  # Override config default (cautious)
            assume_yes=True,
            now=self.now
        )

        self.assertEqual(len(results), 1)

        # Verify audit log shows "full" mode
        with open(audit_path, 'r') as f:
            entries = [json.loads(line) for line in f]

        self.assertEqual(entries[0]["mode"], "full")


if __name__ == '__main__':
    unittest.main()
