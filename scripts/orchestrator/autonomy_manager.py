"""
Autonomy Manager for AI Agent Development Harness

Manages autonomy modes (ask, cautious, full) and approval gates for orchestrator execution.
Provides risk classification, approval decision logic, and audit logging.

Part of v1.2.0 3-Mode Autonomy System
"""

import yaml
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


class AutonomyManager:
    """Manages autonomy mode and approval gates."""

    def __init__(self, config_path: str = "configs/autonomy.yaml", mode_override: Optional[str] = None):
        """
        Initialize AutonomyManager.

        Args:
            config_path: Path to autonomy config file (relative to repo root)
            mode_override: CLI override for mode (ask|cautious|full)

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If mode is invalid
        """
        self.config_path = config_path
        self.config = self._load_config(config_path)
        self.mode = mode_override or self.config.get("mode", "cautious")
        self.decisions_log: List[Dict[str, Any]] = []
        self._validate_mode()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load and parse autonomy config.

        Args:
            config_path: Path to YAML config file

        Returns:
            Parsed config dictionary

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML is malformed

        A relative ``config_path`` is resolved against the current directory first
        (back-compat) and, if not found there, against the harness root (the
        package's location). This keeps the default ``configs/autonomy.yaml``
        working no matter which directory the orchestrator or its tests run from,
        instead of only when invoked from ``harness/``.
        """
        path = Path(config_path)
        if not path.exists() and not path.is_absolute():
            # harness root = parents of scripts/orchestrator/autonomy_manager.py
            harness_root = Path(__file__).resolve().parents[2]
            candidate = harness_root / config_path
            if candidate.exists():
                path = candidate
        if not path.exists():
            raise FileNotFoundError(
                f"Autonomy config not found: {config_path}\n"
                f"Create it using: cp configs/autonomy.yaml.example {config_path}"
            )

        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def _validate_mode(self) -> None:
        """
        Ensure mode is valid.

        Raises:
            ValueError: If mode is not ask|cautious|full
        """
        valid_modes = ["ask", "cautious", "full"]
        if self.mode not in valid_modes:
            raise ValueError(
                f"Invalid autonomy mode '{self.mode}'. "
                f"Must be one of {valid_modes}"
            )

    def should_request_approval(
        self,
        operation: str,
        risk_level: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, str, str]:
        """
        Determine if operation requires user approval.

        Args:
            operation: Operation name (e.g., "edit_file", "git_commit")
            risk_level: Risk level (LOW|MEDIUM|HIGH|CRITICAL)
            context: Optional dict with blast radius, affected files, etc.

        Returns:
            Tuple of (should_ask: bool, reason: str, action: str)
            - should_ask: Whether to prompt user for approval
            - reason: Human-readable explanation
            - action: "proceed" | "ask" | "block"
        """
        mode_config = self.config["modes"][self.mode]

        # CRITICAL in cautious mode → hard block
        if (self.mode == "cautious" and
            risk_level == "CRITICAL" and
            "CRITICAL" in mode_config.get("stop_on_risk_levels", [])):
            self._log_decision(operation, risk_level, "blocked", context)
            return (
                False,
                f"CRITICAL risk operation blocked in cautious mode. "
                f"Use --autonomy full if you accept the risk.",
                "block"
            )

        # Full autonomy → never ask, always proceed
        if self.mode == "full":
            self._log_decision(operation, risk_level, "auto_approved", context)
            return (
                False,
                "Full autonomy mode - auto-approved",
                "proceed"
            )

        # Ask mode → always ask
        if self.mode == "ask":
            return (
                True,
                "Ask mode - all operations require approval",
                "ask"
            )

        # Cautious mode → check risk level
        if self.mode == "cautious":
            auto_approve_levels = mode_config.get("auto_approve_risk_levels", [])
            if risk_level in auto_approve_levels:
                self._log_decision(operation, risk_level, "auto_approved", context)
                return (
                    False,
                    f"{risk_level} risk auto-approved in cautious mode",
                    "proceed"
                )
            else:
                return (
                    True,
                    f"{risk_level} risk requires approval in cautious mode",
                    "ask"
                )

        # Fallback (should not reach here)
        return (True, "Unknown mode behavior", "ask")

    def _log_decision(
        self,
        operation: str,
        risk_level: str,
        decision: str,
        context: Optional[Dict[str, Any]]
    ) -> None:
        """
        Log autonomy decision to audit trail.

        Args:
            operation: Operation name
            risk_level: Risk level (LOW|MEDIUM|HIGH|CRITICAL)
            decision: Decision made (auto_approved|blocked|user_approved|user_rejected)
            context: Optional context dict with blast radius, files, etc.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "mode": self.mode,
            "operation": operation,
            "risk_level": risk_level,
            "decision": decision,
            "context": context or {}
        }
        self.decisions_log.append(entry)

    def log_user_decision(
        self,
        operation: str,
        risk_level: str,
        approved: bool,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log user approval/rejection decision.

        Args:
            operation: Operation name
            risk_level: Risk level
            approved: Whether user approved
            context: Optional context
        """
        decision = "user_approved" if approved else "user_rejected"
        self._log_decision(operation, risk_level, decision, context)

    def save_audit_log(self, output_path: Optional[str] = None) -> None:
        """
        Save audit log to JSONL file.

        Args:
            output_path: Path to output file (default from config)
        """
        if not output_path:
            output_path = self.config.get("audit", {}).get(
                "output_path",
                "runs/autonomy-decisions.jsonl"
            )

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'a') as f:
            for entry in self.decisions_log:
                f.write(json.dumps(entry) + '\n')

        # Clear in-memory log after save
        self.decisions_log = []

    def classify_risk(
        self,
        operation_type: str,
        operation_details: str
    ) -> Optional[str]:
        """
        Classify operation risk based on config.

        Args:
            operation_type: Category (e.g., "file_operations", "git_operations")
            operation_details: Specific operation (e.g., "edit_existing", "commit")

        Returns:
            Risk level (LOW|MEDIUM|HIGH|CRITICAL) or None if unknown
        """
        classifications = self.config.get("risk_classifications", {})
        category = classifications.get(operation_type, {})
        return category.get(operation_details)

    def classify_gitnexus_impact(self, impact_result: Dict[str, Any]) -> str:
        """
        Map GitNexus impact analysis to risk level.

        Args:
            impact_result: Dict from gitnexus_impact() with:
                - affected_symbols: List of symbols
                - affected_processes: List of processes
                - risk: Optional pre-computed risk level

        Returns:
            Risk level (LOW|MEDIUM|HIGH|CRITICAL)
        """
        # If risk already computed by GitNexus, use it
        if "risk" in impact_result:
            return impact_result["risk"]

        # Extract caller count from affected symbols
        affected_symbols = impact_result.get("affected_symbols", [])
        if isinstance(affected_symbols, list):
            caller_count = len(affected_symbols)
        elif isinstance(affected_symbols, dict):
            # Handle dict format: {depth: [symbols]}
            caller_count = sum(len(syms) for syms in affected_symbols.values())
        else:
            caller_count = 0

        # Check for critical path
        affected_processes = impact_result.get("affected_processes", [])
        has_critical_process = any(
            p.get("processType") == "critical" or
            "critical" in p.get("heuristicLabel", "").lower() or
            p.get("priority") == "critical"
            for p in affected_processes
        )

        # Check for security boundary
        has_security = any(
            "auth" in p.get("heuristicLabel", "").lower() or
            "security" in p.get("heuristicLabel", "").lower()
            for p in affected_processes
        )

        # Risk classification
        if has_critical_process or has_security:
            return "CRITICAL"
        elif caller_count >= 25:
            return "CRITICAL"
        elif caller_count >= 10:
            return "HIGH"
        elif caller_count >= 4:
            return "MEDIUM"
        else:
            return "LOW"

    def classify_operation_heuristic(self, operation: str) -> str:
        """
        Classify operation risk using heuristics (fallback when GitNexus unavailable).

        Args:
            operation: Operation name/description

        Returns:
            Risk level (LOW|MEDIUM|HIGH|CRITICAL)
        """
        operation_lower = operation.lower()

        # CRITICAL patterns
        critical_patterns = [
            "force", "critical", "production", "delete_all",
            "drop_database", "reset_hard", "force_push"
        ]
        if any(p in operation_lower for p in critical_patterns):
            return "CRITICAL"

        # HIGH patterns
        high_patterns = [
            "delete", "remove", "push", "deploy", "merge",
            "breaking", "security", "auth"
        ]
        if any(p in operation_lower for p in high_patterns):
            return "HIGH"

        # LOW patterns
        low_patterns = [
            "read", "query", "search", "list", "status",
            "log", "diff", "comment", "documentation"
        ]
        if any(p in operation_lower for p in low_patterns):
            return "LOW"

        # Default to MEDIUM (conservative)
        return "MEDIUM"

    def get_mode_description(self) -> str:
        """
        Get human-readable description of current mode.

        Returns:
            Mode description string
        """
        mode_config = self.config["modes"].get(self.mode, {})
        return mode_config.get("description", self.mode)

    def get_approval_summary(self) -> Dict[str, int]:
        """
        Get summary of decisions from current session.

        Returns:
            Dict with counts: {auto_approved: N, user_approved: N, ...}
        """
        summary = {
            "auto_approved": 0,
            "user_approved": 0,
            "user_rejected": 0,
            "blocked": 0
        }

        for entry in self.decisions_log:
            decision = entry.get("decision", "unknown")
            if decision in summary:
                summary[decision] += 1

        return summary

    def is_always_blocked(self, operation: str) -> bool:
        """
        Check if operation is in always-block list (hard safety guardrail).

        Args:
            operation: Operation name

        Returns:
            True if operation should always be blocked
        """
        always_block = self.config.get("safety", {}).get("always_block", [])
        return operation in always_block


# Convenience function for CLI usage
def create_autonomy_manager(autonomy_mode: Optional[str] = None) -> AutonomyManager:
    """
    Create AutonomyManager instance with optional CLI mode override.

    Args:
        autonomy_mode: Mode from CLI flag (ask|cautious|full) or None

    Returns:
        AutonomyManager instance
    """
    return AutonomyManager(mode_override=autonomy_mode)
