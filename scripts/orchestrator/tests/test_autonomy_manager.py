"""
Unit tests for AutonomyManager

Tests the 3-mode autonomy system (ask, cautious, full) with risk classification,
approval decision logic, and audit logging.

Part of v1.2.0 3-Mode Autonomy System
"""

import unittest
import tempfile
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.orchestrator.autonomy_manager import AutonomyManager


class TestAutonomyManager(unittest.TestCase):
    """Test AutonomyManager class"""

    def test_load_config(self):
        """Config loads and parses correctly."""
        manager = AutonomyManager()
        self.assertIn("modes", manager.config)
        self.assertIn("ask", manager.config["modes"])
        self.assertIn("cautious", manager.config["modes"])
        self.assertIn("full", manager.config["modes"])

    def test_default_mode_is_cautious(self):
        """Default mode is cautious when no override provided."""
        manager = AutonomyManager()
        self.assertEqual(manager.mode, "cautious")

    def test_mode_override(self):
        """CLI mode override works."""
        manager = AutonomyManager(mode_override="ask")
        self.assertEqual(manager.mode, "ask")

        manager = AutonomyManager(mode_override="full")
        self.assertEqual(manager.mode, "full")

    def test_invalid_mode_raises_error(self):
        """Invalid mode raises ValueError."""
        with self.assertRaises(ValueError) as context:
            AutonomyManager(mode_override="invalid")
        self.assertIn("invalid", str(context.exception).lower())

    def test_ask_mode_requires_approval_for_all(self):
        """Ask mode requires approval for all operations regardless of risk."""
        manager = AutonomyManager(mode_override="ask")

        for risk in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
            should_ask, reason, action = manager.should_request_approval(
                "edit_file", risk
            )
            self.assertTrue(should_ask, f"Ask mode should ask for {risk} risk")
            self.assertEqual(action, "ask")

    def test_cautious_mode_auto_approves_low(self):
        """Cautious mode auto-approves LOW risk."""
        manager = AutonomyManager(mode_override="cautious")
        should_ask, reason, action = manager.should_request_approval(
            "read_file", "LOW"
        )
        self.assertFalse(should_ask)
        self.assertEqual(action, "proceed")
        self.assertIn("auto-approved", reason)

    def test_cautious_mode_auto_approves_medium(self):
        """Cautious mode auto-approves MEDIUM risk."""
        manager = AutonomyManager(mode_override="cautious")
        should_ask, reason, action = manager.should_request_approval(
            "edit_file", "MEDIUM"
        )
        self.assertFalse(should_ask)
        self.assertEqual(action, "proceed")

    def test_cautious_mode_asks_for_high(self):
        """Cautious mode asks for HIGH risk approval."""
        manager = AutonomyManager(mode_override="cautious")
        should_ask, reason, action = manager.should_request_approval(
            "delete_file", "HIGH"
        )
        self.assertTrue(should_ask)
        self.assertEqual(action, "ask")

    def test_cautious_mode_blocks_critical(self):
        """Cautious mode blocks CRITICAL risk (hard stop)."""
        manager = AutonomyManager(mode_override="cautious")
        should_ask, reason, action = manager.should_request_approval(
            "force_push", "CRITICAL"
        )
        self.assertFalse(should_ask)  # Doesn't ask, just blocks
        self.assertEqual(action, "block")
        self.assertIn("blocked", reason.lower())

    def test_full_mode_auto_approves_all(self):
        """Full mode auto-approves all risk levels including CRITICAL."""
        manager = AutonomyManager(mode_override="full")

        for risk in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
            should_ask, reason, action = manager.should_request_approval(
                "operation", risk
            )
            self.assertFalse(should_ask, f"Full mode should not ask for {risk}")
            self.assertEqual(action, "proceed")

    def test_classify_gitnexus_impact_low(self):
        """GitNexus impact with 0-3 callers maps to LOW."""
        manager = AutonomyManager()
        impact = {"affected_symbols": [1, 2], "affected_processes": []}
        self.assertEqual(manager.classify_gitnexus_impact(impact), "LOW")

    def test_classify_gitnexus_impact_medium(self):
        """GitNexus impact with 4-9 callers maps to MEDIUM."""
        manager = AutonomyManager()
        impact = {"affected_symbols": [1, 2, 3, 4, 5], "affected_processes": []}
        self.assertEqual(manager.classify_gitnexus_impact(impact), "MEDIUM")

    def test_classify_gitnexus_impact_high(self):
        """GitNexus impact with 10+ callers maps to HIGH."""
        manager = AutonomyManager()
        impact = {"affected_symbols": list(range(15)), "affected_processes": []}
        self.assertEqual(manager.classify_gitnexus_impact(impact), "HIGH")

    def test_classify_gitnexus_impact_critical_path(self):
        """GitNexus impact with critical path maps to CRITICAL."""
        manager = AutonomyManager()
        impact = {
            "affected_symbols": [1, 2],
            "affected_processes": [{"processType": "critical"}]
        }
        self.assertEqual(manager.classify_gitnexus_impact(impact), "CRITICAL")

    def test_classify_gitnexus_impact_critical_callers(self):
        """GitNexus impact with 25+ callers maps to CRITICAL."""
        manager = AutonomyManager()
        impact = {"affected_symbols": list(range(30)), "affected_processes": []}
        self.assertEqual(manager.classify_gitnexus_impact(impact), "CRITICAL")

    def test_classify_risk_file_operations(self):
        """File operations classify correctly."""
        manager = AutonomyManager()
        self.assertEqual(manager.classify_risk("file_operations", "read"), "LOW")
        self.assertEqual(manager.classify_risk("file_operations", "edit_existing"), "LOW")
        self.assertEqual(manager.classify_risk("file_operations", "write_new"), "MEDIUM")
        self.assertEqual(manager.classify_risk("file_operations", "delete"), "HIGH")

    def test_classify_risk_git_operations(self):
        """Git operations classify correctly."""
        manager = AutonomyManager()
        self.assertEqual(manager.classify_risk("git_operations", "status"), "LOW")
        self.assertEqual(manager.classify_risk("git_operations", "commit"), "MEDIUM")
        self.assertEqual(manager.classify_risk("git_operations", "push"), "HIGH")
        self.assertEqual(manager.classify_risk("git_operations", "force_push"), "CRITICAL")

    def test_classify_operation_heuristic(self):
        """Heuristic risk classification works as fallback."""
        manager = AutonomyManager()

        # LOW patterns
        self.assertEqual(manager.classify_operation_heuristic("read file"), "LOW")
        self.assertEqual(manager.classify_operation_heuristic("list directory"), "LOW")

        # MEDIUM (default)
        self.assertEqual(manager.classify_operation_heuristic("edit file"), "MEDIUM")

        # HIGH patterns
        self.assertEqual(manager.classify_operation_heuristic("delete file"), "HIGH")
        self.assertEqual(manager.classify_operation_heuristic("git push"), "HIGH")

        # CRITICAL patterns
        self.assertEqual(manager.classify_operation_heuristic("force push"), "CRITICAL")
        self.assertEqual(manager.classify_operation_heuristic("production deploy"), "CRITICAL")

    def test_audit_log_written(self):
        """Audit log saves to JSONL correctly."""
        manager = AutonomyManager(mode_override="full")

        # Trigger some decisions
        manager.should_request_approval("edit_file", "MEDIUM")
        manager.should_request_approval("delete_file", "HIGH")

        # Save to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            log_path = f.name

        try:
            manager.save_audit_log(log_path)

            # Read and verify
            with open(log_path, 'r') as f:
                entries = [json.loads(line) for line in f]

            self.assertEqual(len(entries), 2)
            self.assertEqual(entries[0]["mode"], "full")
            self.assertEqual(entries[0]["risk_level"], "MEDIUM")
            self.assertEqual(entries[0]["decision"], "auto_approved")
            self.assertEqual(entries[1]["risk_level"], "HIGH")

            # Verify JSONL format (one entry per line)
            with open(log_path, 'r') as f:
                lines = f.readlines()
            self.assertEqual(len(lines), 2)

        finally:
            # Cleanup
            Path(log_path).unlink(missing_ok=True)

    def test_audit_log_includes_context(self):
        """Audit log includes context when provided."""
        manager = AutonomyManager(mode_override="full")

        context = {
            "files": ["core/auth.py"],
            "impact": {"callers": 5, "processes": 2}
        }

        manager.should_request_approval("edit_file", "MEDIUM", context)

        self.assertEqual(len(manager.decisions_log), 1)
        self.assertEqual(manager.decisions_log[0]["context"], context)

    def test_log_user_decision(self):
        """User approval/rejection is logged correctly."""
        manager = AutonomyManager()

        manager.log_user_decision("edit_file", "HIGH", approved=True)
        self.assertEqual(manager.decisions_log[-1]["decision"], "user_approved")

        manager.log_user_decision("delete_file", "HIGH", approved=False)
        self.assertEqual(manager.decisions_log[-1]["decision"], "user_rejected")

    def test_get_approval_summary(self):
        """Approval summary counts decisions correctly."""
        manager = AutonomyManager(mode_override="cautious")

        # Trigger various decisions
        manager.should_request_approval("read", "LOW")  # auto_approved
        manager.should_request_approval("edit", "MEDIUM")  # auto_approved
        manager.should_request_approval("critical_op", "CRITICAL")  # blocked
        manager.log_user_decision("delete", "HIGH", approved=True)  # user_approved

        summary = manager.get_approval_summary()
        self.assertEqual(summary["auto_approved"], 2)
        self.assertEqual(summary["blocked"], 1)
        self.assertEqual(summary["user_approved"], 1)
        self.assertEqual(summary["user_rejected"], 0)

    def test_get_mode_description(self):
        """Mode description is returned correctly."""
        manager = AutonomyManager(mode_override="cautious")
        desc = manager.get_mode_description()
        # Description should mention autonomous and low-risk
        self.assertIn("autonomous", desc.lower())
        self.assertIn("low-risk", desc.lower())

    def test_decisions_log_cleared_after_save(self):
        """In-memory decisions log is cleared after save."""
        manager = AutonomyManager(mode_override="full")

        manager.should_request_approval("edit", "MEDIUM")
        self.assertEqual(len(manager.decisions_log), 1)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            log_path = f.name

        try:
            manager.save_audit_log(log_path)
            self.assertEqual(len(manager.decisions_log), 0)  # Cleared
        finally:
            Path(log_path).unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()
