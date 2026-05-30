# Eval Case: Invalid Route Handling

## Purpose

Test whether the orchestrator (Phase 02/03) handles invalid route requests
gracefully. Users may typo route names, reference deprecated routes, or request
routes that don't exist in `configs/routing.yaml`. The orchestrator should
provide helpful feedback, not crash or silently ignore the request.

## Input

Test various invalid route scenarios:

1. **Non-existent route name:**
   ```bash
   python3 scripts/orchestrate.py route nonexistent_route
   ```

2. **Typo in route name:**
   ```bash
   python3 scripts/orchestrate.py route task_defination  # missing 'i'
   python3 scripts/orchestrate.py route agentdesign       # missing underscore
   ```

3. **Empty route name:**
   ```bash
   python3 scripts/orchestrate.py route ""
   ```

4. **Route with missing stage definition:**
   ```yaml
   # configs/routing.yaml has route referencing non-existent stage
   broken_route:
     stages: ["99-nonexistent-stage"]
     steps: []
   ```

5. **Route with malformed steps:**
   ```yaml
   # Route missing required 'agent' field in step
   broken_route:
     stages: ["01-task-definition"]
     steps:
       - prompt: prompts/research/v1.md  # missing 'agent' field
   ```

## Expected Behavior

For each invalid route scenario, the orchestrator should:

- **Detect the invalid route** during route resolution
- **Provide helpful error message** including:
  - What was requested vs. what's available
  - List of valid route names (for typos/not-found)
  - Suggestion to check `configs/routing.yaml`
- **Exit with non-zero code**
- **Not attempt execution** of a malformed route

Helpful error message example:
```
Error: Route 'task_defination' not found in configs/routing.yaml

Available routes:
  - task_definition
  - agent_design
  - prompt_design
  - tool_integration
  - evaluation
  - iteration
  - release

Did you mean: task_definition?
```

## Test Execution

```bash
# Test non-existent route
python3 scripts/orchestrate.py route nonexistent_route 2>&1 | grep -i "not found"
echo $?  # Should be non-zero

# Test empty route
python3 scripts/orchestrate.py route "" 2>&1
echo $?  # Should be non-zero

# Test route with missing stage (requires modified config)
# Create temporary config with broken route definition
# Verify error is caught during route resolution
```

## Example Outputs

### Non-Existent Route
```
Error: Route 'nonexistent_route' not found in configs/routing.yaml

Available routes:
  - task_definition
  - agent_design
  - prompt_design
  - tool_integration
  - evaluation
  - iteration
  - release

Run: python3 scripts/orchestrate.py --help
```

### Typo with Suggestion
```
Error: Route 'task_defination' not found in configs/routing.yaml

Did you mean: task_definition?

Available routes:
  - task_definition  ← closest match
  - agent_design
  - prompt_design
  - tool_integration
  - evaluation
  - iteration
  - release
```

### Empty Route Name
```
Error: Invalid route name ''

Usage: python3 scripts/orchestrate.py route <route-name> [OPTIONS]

Available routes:
  - task_definition
  - agent_design
  - prompt_design
  - tool_integration
  - evaluation
  - iteration
  - release

Run: python3 scripts/orchestrate.py --help
```

## Rubric

Use `evals/rubrics/orchestrator-output-quality.md`. Focus on:

- **Route resolution correctness** (score 4+): Invalid routes rejected cleanly
- **Failure transparency** (score 4+): Clear error messages with helpful suggestions
- **Safety adherence** (score 4+): No execution of malformed routes

## Pass Criteria

- Non-existent routes produce clear "not found" errors
- Error messages list available routes
- Typos produce "did you mean?" suggestions where applicable
- Malformed route definitions (missing required fields) are caught during resolution
- Exit codes are non-zero for all invalid route scenarios
- Valid routes continue to work (no false positives)
- Help text is clear and actionable
