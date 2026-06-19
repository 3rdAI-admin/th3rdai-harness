# Aider Adaptation Guide

**Environment:** Aider (CLI-based AI coding assistant)
**Compatibility:** ✅ Excellent (98% compatible - BEST fit for orchestrator)
**Effort:** 30 minutes for basic setup, 2-3 hours for full optimization

## Overview

Aider is the **ideal environment** for the AI Agent Development Harness. As a CLI-based tool, it integrates perfectly with the orchestrator with zero friction. Aider was designed for exactly the kind of workflow the harness implements.

## Why Aider is Perfect for the Harness

1. **CLI-native:** The orchestrator can call aider directly
2. **Context management:** Aider automatically tracks file changes
3. **Git integration:** Built-in commit workflow aligns with harness release stage
4. **Model-agnostic:** Works with Claude, GPT-4, local models, etc.
5. **Minimal configuration:** Works out of the box

## Quick Start (10 minutes)

### 1. Install Aider

```bash
# Install via pip
pip install aider-chat

# Or via pipx (recommended for isolated install)
pipx install aider-chat

# Verify installation
aider --version
```

### 2. Configure API Keys

```bash
# For Claude (Anthropic)
export ANTHROPIC_API_KEY=your-key-here

# For OpenAI
export OPENAI_API_KEY=your-key-here

# Or create .env file in harness root
cat > .env << 'EOF'
ANTHROPIC_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here
EOF
```

### 3. Configure Orchestrator for Aider

```yaml
# configs/execution.yaml
execution:
  default_adapter: cli
  cli:
    command: ["aider", "--yes", "--message"]
    timeout_seconds: 300
    env_allowlist:
      - PATH
      - HOME
      - ANTHROPIC_API_KEY
      - OPENAI_API_KEY
```

### 4. Test Integration

```bash
# Dry run to see context bundles
python3 scripts/orchestrate.py route iteration

# Execute with aider
python3 scripts/orchestrate.py route iteration --execute --adapter cli --autonomy cautious
```

**That's it!** Aider is now fully integrated.

## Aider Configuration

### Recommended `.aider.conf.yml`

Create in the harness root:

```yaml
# .aider.conf.yml - Aider configuration for harness

# Model selection (choose one)
model: claude-3-5-sonnet-20241022  # Recommended
# model: gpt-4-turbo-preview
# model: deepseek/deepseek-chat     # For local/open-source

# Git integration
auto-commits: false  # Let harness control commits
dirty-commits: true  # Allow working with dirty git state
auto-lint: false     # Orchestrator handles validation

# Context management
show-diffs: true
pretty: true
stream: false  # Better for orchestrator execution

# Edit format
edit-format: diff  # Fast, precise edits

# File management
read-only-files:
  - "FRAMEWORK.md"
  - "CONTEXT.md"
  - "configs/*.yaml"
  - "evals/rubrics/*.md"

# Excluded files
no-auto-commits:
  - "runs/*.md"
  - ".env"
  - "*.pyc"
```

### Model-Specific Configurations

**For Claude (Recommended for harness work):**

```bash
# Set default model
export AIDER_MODEL=claude-3-5-sonnet-20241022

# Or in .aider.conf.yml
model: claude-3-5-sonnet-20241022
```

**For GPT-4:**

```bash
export AIDER_MODEL=gpt-4-turbo-preview
```

**For Local Models (via Ollama):**

```bash
# Install Ollama first: https://ollama.ai

# Pull a model
ollama pull deepseek-coder-v2

# Configure aider
export AIDER_MODEL=ollama/deepseek-coder-v2
```

## Using Aider with the Harness

### Method 1: Via Orchestrator (Recommended)

The orchestrator assembles context and calls aider automatically:

```bash
# Execute a route with aider
python3 scripts/orchestrate.py route iteration --execute --adapter cli --autonomy cautious

# What happens:
# 1. Orchestrator reads routing.yaml and plans steps
# 2. For each step, assembles context bundle:
#    - Agent contract
#    - Skill procedure
#    - Prompt template
#    - Stage context
#    - Previous outputs
# 3. Calls: aider --yes --message "$(cat context.md)"
# 4. Aider executes the step
# 5. Orchestrator records the result in runs/
# 6. Autonomy manager logs decision in runs/autonomy-decisions.jsonl
```

**Example orchestrator output:**

```
Autonomy mode: cautious (Autonomous for low-risk, ask for high-risk, block critical)
✓ Step 1 (planner): MEDIUM risk auto-approved
Executing: aider --yes --message "..."
[Aider output]
  step 1 planner: executed -> /runs/20260619-iteration-01-planner.md
✓ Step 2 (builder): MEDIUM risk auto-approved
Executing: aider --yes --message "..."
[Aider output]
  step 2 builder: executed -> /runs/20260619-iteration-02-builder.md
Autonomy summary: 2 auto-approved, 0 user-approved, 0 rejected, 0 blocked
```

### Method 2: Interactive Aider with Agent Context

Run aider manually and give it agent context:

```bash
# Start aider in the repo
cd ~/projects/th3rdai-harness
aider

# Load agent contract
> /add agents/builder.agent.md
> /add stages/06-iteration/CONTEXT.md

# Give instructions
> Act as the Builder agent and implement the autonomy system Phase A according to stages/06-iteration/output/AUTOPLAN.md

# Aider will:
# - Read the agent contract
# - Understand the stage context
# - Follow the plan
# - Make file edits
```

### Method 3: Aider with Specific Files

```bash
# Start aider with specific files to edit
aider scripts/orchestrator/driver.py scripts/orchestrate.py

# Give instructions
> Add autonomy_mode parameter to execute_route() and integrate AutonomyManager

# Aider will:
# - Make precise edits to both files
# - Show diffs
# - Apply changes
```

## Harness-Specific Aider Workflows

### Workflow 1: Implementing a Plan

```bash
# 1. Create the plan (manually or via planner agent)
aider
> /add agents/planner.agent.md
> /add stages/01-task-definition/output/task-definition.md
> Create an implementation plan in stages/06-iteration/output/AUTOPLAN.md
> /exit

# 2. Execute the plan via orchestrator
python3 scripts/orchestrate.py route iteration --execute --adapter cli --autonomy cautious

# 3. Review outputs
ls -la runs/
cat runs/autonomy-decisions.jsonl
```

### Workflow 2: Agent-Driven Development

```bash
# Builder agent session
aider
> /add agents/builder.agent.md
> /add stages/06-iteration/output/AUTOPLAN.md
> Act as the Builder agent. Implement Phase A of AUTOPLAN.md. Follow all constraints in the agent contract.

# Aider follows:
# - Agent permissions (what tools are allowed)
# - Agent scope (IN SCOPE / OUT OF SCOPE)
# - Agent operating rules
# - Success criteria
```

### Workflow 3: Iterative Refinement

```bash
# Start with initial implementation
aider src/feature.py

> Implement basic authentication flow

# Run tests
> /run python3 -m pytest tests/test_auth.py

# Fix issues based on test results
> Fix the failing test_invalid_token test

# Validate
> /run bash scripts/07-validate-harness.sh
```

### Workflow 4: Multi-Stage Workflow

```bash
# Stage 1: Task Definition
aider
> /add agents/researcher.agent.md
> /add stages/01-task-definition/CONTEXT.md
> Research authentication best practices and create task-definition.md in stages/01-task-definition/output/
> /exit

# Stage 2: Planning
aider
> /add agents/planner.agent.md
> /add stages/01-task-definition/output/task-definition.md
> /add stages/06-iteration/CONTEXT.md
> Create an implementation plan in stages/06-iteration/output/AUTOPLAN.md
> /exit

# Stage 3: Implementation via orchestrator
python3 scripts/orchestrate.py route iteration --execute --adapter cli --autonomy full --yes
```

## Aider Commands Reference

### Essential Commands

```bash
# File management
/add <file>          # Add file to chat context
/drop <file>         # Remove file from context
/ls                  # List files in context

# Execution
/run <command>       # Run shell command and include output
/commit              # Manually commit changes

# Context
/read-only <file>    # Add file as read-only (won't be edited)
/web <url>           # Fetch and include web page content

# Session management
/clear               # Clear chat history
/exit                # Exit aider

# Settings
/model <name>        # Switch model
/architect           # Switch to architect mode (plan only)
/code                # Switch to code mode (implement)
```

### Useful Aider Flags

```bash
# Start with specific model
aider --model claude-3-5-sonnet-20241022

# Auto-add git files
aider --auto-commits

# Specific edit format
aider --edit-format diff  # Fast, precise
aider --edit-format whole  # Replace entire file
aider --edit-format udiff  # Unified diff format

# Message without interactive mode
aider --yes --message "Implement feature X"

# Read-only mode (for research)
aider --read agents/builder.agent.md --read stages/06-iteration/CONTEXT.md

# Stream output (for interactive use)
aider --stream

# No streaming (better for orchestrator)
aider --no-stream
```

## Advanced Orchestrator Integration

### Custom Context Assembly

The orchestrator automatically assembles context, but you can customize it:

```python
# scripts/orchestrator/sequencer.py - customize build_context()

def build_context(step):
    """Assemble context bundle for a step."""
    # Default includes:
    # - Agent contract
    # - Skill
    # - Prompt
    # - Stage context
    # - Previous outputs

    # You can add custom context here:
    bundle.add_input("custom/context.md")

    return bundle
```

### Pre/Post Step Hooks

Add hooks in the orchestrator for validation:

```python
# scripts/orchestrator/driver.py - add before/after step execution

def execute_route(route_name, adapter, ...):
    for step in steps:
        # PRE-STEP HOOK
        if step.agent == "builder":
            # Run linter before builder steps
            subprocess.run(["ruff", "check", "."])

        result = adapter.run(bundle, ...)

        # POST-STEP HOOK
        if result.status == "executed":
            # Run tests after successful execution
            subprocess.run(["pytest", "-x"])
```

### Conditional Autonomy

Use different autonomy modes per step:

```python
# Determine autonomy mode based on step
autonomy_mode = "ask" if step.agent == "builder" else "cautious"

results = driver.execute_route(
    route_name, adapter,
    autonomy_mode=autonomy_mode
)
```

## Best Practices for Aider + Harness

### 1. Use Architect Mode for Planning

```bash
# Switch to architect mode for planning phases
aider --architect agents/planner.agent.md
> Create implementation plan for feature X

# Switch to code mode for implementation
aider --code
> Implement the plan
```

### 2. Add Context Files Read-Only

```bash
# Prevent accidental edits to reference docs
aider --read FRAMEWORK.md --read agents/builder.agent.md
> Implement feature following the framework
```

### 3. Use /run for Validation

```bash
aider
> Implement authentication

# Validate after each change
> /run python3 -m pytest tests/test_auth.py
> /run bash scripts/07-validate-harness.sh
```

### 4. Commit After Major Milestones

```bash
aider --auto-commits
# Or manually:
> /commit -m "feat: implement authentication system"
```

### 5. Use Aider's Git Integration

Aider works great with the harness release workflow:

```bash
# Aider will:
# - Only edit tracked files (respects .gitignore)
# - Show diffs clearly
# - Optionally auto-commit

# Harness release workflow:
1. Implement via aider
2. /run bash scripts/07-validate-harness.sh
3. /commit -m "feat: new feature"
4. Manual: git push
```

## Performance Optimization

### 1. Use --no-stream for Orchestrator

```yaml
# configs/execution.yaml
execution:
  cli:
    command: ["aider", "--yes", "--no-stream", "--message"]
```

Faster for programmatic execution.

### 2. Limit Context Size

```yaml
# .aider.conf.yml
map-tokens: 1024  # Limit token budget for repo map
max-chat-history-tokens: 4096  # Limit history
```

### 3. Use Faster Models for Simple Tasks

```bash
# Use GPT-3.5 for simple refactors
aider --model gpt-3.5-turbo --message "Rename function X to Y"

# Use Claude Opus for complex tasks
aider --model claude-opus-20240229 --message "Implement complex feature Z"
```

### 4. Reuse Aider Sessions

Instead of spawning new aider per step, reuse a session:

```python
# Advanced: Custom adapter that reuses aider process
class PersistentAiderAdapter(Adapter):
    def __init__(self):
        self.process = subprocess.Popen(
            ["aider", "--yes"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

    def run(self, bundle, ...):
        # Send message to existing aider process
        # Return result
```

## Troubleshooting

### Issue: Aider makes too many changes

**Solution:** Be specific in orchestrator context bundles:

```markdown
# In assembled context:

## Constraints
- ONLY modify scripts/orchestrator/driver.py
- DO NOT touch config files
- DO NOT refactor unrelated code
```

### Issue: Aider can't find files

**Solution:** Aider works relative to repo root. Ensure orchestrator runs from root:

```python
# scripts/orchestrator/config.py already handles this
def repo_root():
    """Find git repo root."""
    # ... returns Path to root
```

### Issue: API rate limits

**Solution:** Configure retry logic or use local models:

```bash
# Use Ollama for unlimited local execution
export AIDER_MODEL=ollama/deepseek-coder-v2

# Or add retry to orchestrator
# configs/execution.yaml
execution:
  cli:
    timeout_seconds: 600  # Longer timeout
    retry_count: 3
```

### Issue: Aider commits when it shouldn't

**Solution:** Disable auto-commits:

```yaml
# .aider.conf.yml
auto-commits: false
```

The harness controls when commits happen (via release stage).

## Example: Complete Feature Implementation

```bash
# Full workflow: Idea → Implementation → Release

# 1. Task Definition (manual aider)
aider
> /add agents/researcher.agent.md
> /add stages/01-task-definition/CONTEXT.md
> Research deployment automation and create task definition
> /exit

# 2. Planning (manual aider)
aider
> /add agents/planner.agent.md
> /add stages/01-task-definition/output/task-definition.md
> Create implementation plan in stages/06-iteration/output/AUTOPLAN.md
> /exit

# 3. Implementation (orchestrator with aider)
python3 scripts/orchestrate.py route iteration --execute --adapter cli --autonomy cautious

# 4. Review outputs
cat runs/autonomy-decisions.jsonl
ls -la stages/06-iteration/output/

# 5. Validation
bash scripts/07-validate-harness.sh
python3 -m pytest scripts/orchestrator/tests/ -v

# 6. Release (manual aider)
aider
> /add agents/reviewer.agent.md
> Review the implementation for release readiness
> /commit -m "feat: deployment automation system"
> /exit

# 7. Push
git push origin main
```

## Aider + Harness Advantages

**Why Aider is the best fit:**

1. ✅ **Zero-friction orchestrator integration** - CLI-native
2. ✅ **Precise edits** - diff/udiff format minimizes changes
3. ✅ **Git-aware** - Understands repo context
4. ✅ **Model-agnostic** - Works with Claude, GPT-4, local models
5. ✅ **Context management** - Automatic file tracking
6. ✅ **Validation-friendly** - `/run` command for tests
7. ✅ **No IDE lock-in** - Works with any editor
8. ✅ **Fast** - No GUI overhead
9. ✅ **Scriptable** - Perfect for automation
10. ✅ **Open source** - Customizable and extensible

## Summary

**Aider Compatibility:** ✅ 98% (best fit for harness)

**Setup Time:**
- Basic: 30 minutes
- Full optimization: 2-3 hours

**Recommended Configuration:**
1. Install aider: `pip install aider-chat`
2. Configure API keys (Claude/OpenAI)
3. Create `.aider.conf.yml` with recommended settings
4. Configure `configs/execution.yaml` for orchestrator
5. Test with: `python3 scripts/orchestrate.py route iteration --execute`

**Best Used For:**
- ✅ Automated orchestrator execution
- ✅ CLI-driven workflows
- ✅ Precise, targeted code changes
- ✅ Git-integrated development
- ✅ Multi-model experimentation
- ✅ Headless/server environments

**Aider is the GOLD STANDARD** for harness execution. It was practically made for this workflow.
