# Eval Case: Missing Reference Detection

## Purpose

Test whether the orchestrator (Phase 02 sequencer) fails transparently when
referenced files (contracts, skills, prompts, model profiles) don't exist.
The orchestrator should detect and report missing dependencies before attempting
to execute a route, not fail mid-execution with cryptic errors.

## Input

Create test scenarios with missing references:

1. **Missing agent contract:**
   ```yaml
   # configs/agents.yaml
   researcher:
     contract: agents/missing-researcher.md  # file doesn't exist
     default_skill: skills/research/research.md
   ```

2. **Missing skill file:**
   ```yaml
   researcher:
     contract: agents/researcher.md
     default_skill: skills/research/missing-skill.md  # file doesn't exist
   ```

3. **Missing prompt version:**
   ```yaml
   # configs/routing.yaml
   task_definition:
     stages: ["01-task-definition"]
     steps:
       - agent: researcher
         prompt: prompts/research/v999.md  # version doesn't exist
   ```

4. **Missing model profile:**
   ```yaml
   # configs/agents.yaml
   researcher:
     contract: agents/researcher.md
     model_profile: models/profiles/missing-profile.md  # doesn't exist
   ```

5. **Missing stage inputs:**
   ```yaml
   # Stage contract references non-existent input file
   inputs:
     - shared/missing-context.md
   ```

## Expected Behavior

For each missing reference, the orchestrator should:

- **Detect the missing file** during route resolution (before execution)
- **Report the reference chain** (e.g., "route task_definition → agent researcher → contract agents/missing-researcher.md not found")
- **Exit early with clear error** (don't attempt to continue)
- **List the expected path** (repo-root-relative) in the error message
- **Return non-zero exit code**

## Test Execution

```bash
# Create test config with missing references
mkdir -p /tmp/orchestrator-missing-test/configs
cp configs/*.yaml /tmp/orchestrator-missing-test/configs/
# Modify copied config to reference non-existent file

# Should fail with clear error before execution:
python3 scripts/orchestrate.py route task_definition --config-dir /tmp/orchestrator-missing-test/configs

# Error should include:
# - Which file is missing
# - What referenced it (route → agent → field)
# - Expected repo-relative path
```

## Example Outputs

### Missing Contract Error
```
Error: Missing file referenced in route resolution

Route: task_definition
  Step 1: agent 'researcher'
    Field: contract
    Path: agents/missing-researcher.md
    Status: NOT FOUND

Expected file at: /path/to/repo/agents/missing-researcher.md

Reference chain:
  configs/routing.yaml → route 'task_definition'
    → step 1 → agent 'researcher'
      → configs/agents.yaml → researcher.contract
        → agents/missing-researcher.md (NOT FOUND)
```

### Missing Skill Error
```
Error: Missing file referenced in route resolution

Route: task_definition
  Step 1: agent 'researcher'
    Field: default_skill
    Path: skills/research/missing-skill.md
    Status: NOT FOUND

Expected file at: /path/to/repo/skills/research/missing-skill.md

Check:
  - File path in configs/agents.yaml (researcher.default_skill)
  - Spelling and capitalization
  - File exists in repository
```

## Rubric

Use `evals/rubrics/orchestrator-output-quality.md`. Focus on:

- **Failure transparency** (score 4+): Missing files reported clearly with reference chain
- **Route resolution correctness** (score 4+): Validates all references exist before proceeding
- **Path correctness** (score 4+): Error messages use repo-relative paths
- **Safety adherence** (score 4+): No partial execution with missing dependencies

## Pass Criteria

- All missing files detected before route execution begins
- Error messages include reference chain (route → agent → field → path)
- Repo-relative paths used in error reporting
- No cryptic "file not found" errors from deep in the stack
- Non-zero exit code for all missing reference scenarios
- Valid routes with all references present are not rejected (no false positives)
