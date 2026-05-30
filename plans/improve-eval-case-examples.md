# Plan: Add Example Outputs to Orchestrator Eval Cases

## Goal

Enhance 3 orchestrator eval cases by adding concrete example outputs to make them easier to run and validate.

## Scope

**In Scope:**
- Add example error messages to `malformed-config.md`
- Add example missing reference errors to `missing-references.md`
- Add example "did you mean?" output to `invalid-route.md`

**Out of Scope:**
- Running the actual tests (just document examples)
- Modifying other eval cases
- Changing rubric criteria

## Implementation Steps

### Step 1: Add Examples to malformed-config.md

**File:** `evals/cases/orchestrator/malformed-config.md`

**Add section before "Rubric":**

```markdown
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
```

### Step 2: Add Examples to missing-references.md

**File:** `evals/cases/orchestrator/missing-references.md`

**Add section before "Rubric":**

```markdown
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
```

### Step 3: Add Examples to invalid-route.md

**File:** `evals/cases/orchestrator/invalid-route.md`

**Add section before "Rubric":**

```markdown
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
```

## Validation

After implementing:

1. **Visual inspection:**
   ```bash
   cat evals/cases/orchestrator/malformed-config.md
   cat evals/cases/orchestrator/missing-references.md
   cat evals/cases/orchestrator/invalid-route.md
   ```

2. **Validator passes:**
   ```bash
   scripts/07-validate-harness.sh
   # Expected: 98/98 passes
   ```

3. **Markdown renders correctly:**
   - Code blocks are properly formatted
   - Examples are readable
   - Syntax highlighting works

## Success Criteria

- [ ] All 3 files have "Example Outputs" section
- [ ] Examples show realistic error messages with context
- [ ] Code blocks are properly formatted with triple backticks
- [ ] Validator still passes
- [ ] No breaking changes to existing eval cases

## Effort

**Estimated time:** 15-20 minutes
**Complexity:** Low
**Risk:** Low (documentation-only changes)

## Notes

- Keep examples realistic but concise
- Show line numbers and file paths in errors
- Include helpful suggestions where appropriate
- Use consistent error message format across examples
