# Rubric: Orchestrator Output Quality

Scores the artifacts produced by the Native Orchestrator (config parses, context
bundles, and run records) — not agent reasoning. Use this rubric for eval cases
under `evals/cases/orchestrator/`.

Score each category from 1 to 5.

| Score | Meaning |
|-------|---------|
| 1 | Missing or incorrect — would corrupt downstream steps |
| 2 | Weak; major fixes needed before use |
| 3 | Usable with gaps |
| 4 | Strong with minor gaps |
| 5 | Correct, complete, and reproducible |

## Criteria

- **Route resolution correctness** — every agent in the route resolves to a real contract, default skill, and model profile.
- **Context bundle completeness** — each step bundle includes contract + skill procedure + prompt version + model profile + declared inputs.
- **Config parse fidelity** — the flat-YAML subset is parsed correctly, including edge cases (`requires_approval: []` → empty list, comment headers with colons, multiple top-level keys, nested lists).
- **Run-record schema conformance** — emitted records validate against `telemetry/run-log-schema.md` (required fields present, correct value domains).
- **Path correctness** — all persisted paths are repo-root-relative; no absolute, machine-specific paths.
- **Failure transparency** — missing referenced files are reported with context, never silently skipped or guessed.
- **Safety adherence** — dry-run invokes no model/network/installs; approval-gated actions are not performed without approval.
- **Reproducibility** — re-running a dry-run over unchanged inputs yields equivalent bundles/records (modulo timestamps/run-ids).

## Pass Threshold

The orchestrator output passes when:

- No criterion scores below 3.
- Average score is 4 or higher.
- Config parse fidelity and run-record schema conformance both score 4 or higher
  (these are correctness-critical; gaps here corrupt downstream steps).
