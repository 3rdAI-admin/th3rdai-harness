# Eval Case: Config Subset Parsing Fidelity

## Purpose

Test whether the orchestrator's stdlib-only config reader (Phase 01) correctly
parses the real `configs/*.yaml` files, including the known edge cases that a
naive `key: value` splitter would corrupt. This case doubles as a permanent
regression guard for the config audit performed during planning.

## Input

Parse all four config files and assert structure:

```
python3 -c "from scripts.orchestrator import config; print(config.load_tools())"
python3 -c "from scripts.orchestrator import config; print(config.load_models())"
python3 -c "from scripts.orchestrator import config; print(config.load_agents())"
python3 -c "from scripts.orchestrator import config; print(config.load_routing())"
```

## Expected Qualities

- **`requires_approval: []` in `configs/tools.yaml` parses to an empty list**, not the string `"[]"`. (Round-trip write/read preserves it as a list.)
- The comment header in `configs/models.yaml` (lines with `#` that themselves contain colons and `#`) is skipped, not parsed as data.
- `configs/tools.yaml`'s two top-level keys (`tool_policies` and `safety_rules`) are both returned; the loader does not assume a single root.
- Three levels of nesting (`tool_policies → <policy> → allowed → [items]`) are preserved.
- Numeric scalars (`temperature: 0.0 / 0.1 / 0.2`) are handled consistently (documented as string or float, round-trips faithfully).
- Unsupported syntax fails loudly with line context — never silently misparsed.
- A synthetic `null` value parses to `None` (no live config uses `null` today).

## Rubric

Use `evals/rubrics/orchestrator-output-quality.md`. Config parse fidelity must
score 4 or higher to pass (correctness-critical).
