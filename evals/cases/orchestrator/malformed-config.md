# Eval Case: Malformed Config Error Handling

## Purpose

Test whether the orchestrator's config reader (Phase 01) fails transparently when
encountering malformed YAML syntax. The orchestrator should never silently skip
errors, guess at structure, or corrupt downstream steps with partial parses.

## Input

Create temporary malformed config files and attempt to parse them:

1. **Inconsistent indentation:**
   ```yaml
   agents:
     researcher:
       contract: agents/researcher.md
      role: Research  # wrong indent
   ```

2. **Unsupported YAML features (anchors/aliases):**
   ```yaml
   base: &base
     timeout: 120
   agent:
     <<: *base  # anchor/alias not in subset
   ```

3. **Multiline strings without proper syntax:**
   ```yaml
   description: This is a
   multiline description  # missing | or >
   without proper syntax
   ```

4. **Invalid list syntax:**
   ```yaml
   routes:
     - task_definition
     - agent_design
     missing_dash_here
   ```

## Expected Behavior

For each malformed input, the orchestrator should:

- **Fail loudly** with a clear error message (not silent corruption)
- **Report line context** where possible (e.g., "line 4: inconsistent indent")
- **Not produce partial output** (no half-parsed configs)
- **Return non-zero exit code** if invoked via CLI
- **Raise appropriate exception** if invoked via Python API (YAMLSubsetError or similar)

## Test Execution

```bash
# Create temporary malformed configs in a test directory
mkdir -p /tmp/orchestrator-error-test
# Write malformed YAML to test files
# Attempt to parse and verify error reporting

# Should fail with clear error:
python3 -c "from scripts.orchestrator import config; config.load_yaml_file('/tmp/orchestrator-error-test/bad.yaml')"

# CLI should exit non-zero:
python3 scripts/orchestrate.py route task_definition --config-dir /tmp/orchestrator-error-test
echo $?  # Should be non-zero
```

## Example Outputs

### Inconsistent Indentation Error
```
Error: YAML parse error in configs/agents.yaml
Line 4: Inconsistent indentation
  Expected 2 spaces, found 1 space

  3: researcher:
  4:  role: Research  # ← inconsistent indent
  5:   contract: agents/researcher.md
```

### Unsupported Feature Error
```
Error: YAML parse error in configs/agents.yaml
Line 2: Anchors and aliases not supported

  1: base: &base
  2:   timeout: 120  # ← anchor/alias syntax not in subset
  3: agent:
  4:   <<: *base

The orchestrator YAML parser supports only:
- Nested mappings and lists
- Scalar values (strings, numbers, booleans, null)
- Comments (# prefix)

Use explicit duplication or generate configs if advanced YAML features are needed.
```

## Rubric

Use `evals/rubrics/orchestrator-output-quality.md`. Focus on:

- **Failure transparency** (score 4+): Errors reported with context, never silent
- **Config parse fidelity** (score 4+): No partial/corrupted parses accepted
- **Safety adherence** (score 4+): No downstream corruption from bad input

## Pass Criteria

- All malformed inputs produce clear error messages
- No silent failures or partial parses
- Error messages include line numbers or context where possible
- Exit codes/exceptions are appropriate for programmatic detection
- No valid config is rejected (no false positives)
