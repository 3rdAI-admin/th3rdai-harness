# Windsurf Adaptation Guide

**Environment:** Windsurf (Codeium AI IDE)
**Compatibility:** ✅ High (90% compatible)
**Effort:** 1-2 hours for basic setup, 3-5 hours for full adaptation

## Overview

Windsurf is Codeium's AI-native IDE with excellent context awareness and multi-file editing capabilities. The AI Agent Development Harness integrates naturally with Windsurf's collaborative coding approach.

## Quick Start (20 minutes)

### 1. Initial Setup

```bash
# Open your harness workspace in Windsurf
cd ~/projects/th3rdai-harness

# Create Windsurf-specific configuration
cp CLAUDE.md WINDSURF.md
```

### 2. Update WINDSURF.md

```markdown
# AI Agent Development Harness

## Identity

You are an AI assistant working inside an AI Agent Development Harness via Windsurf. Your role is to help design, implement, evaluate, and improve reusable AI agents, prompts, skills, model profiles, and evaluation workflows.

## Environment: Windsurf (Codeium)

This workspace uses Windsurf's AI capabilities with the harness methodology:
- Use Cascade (Windsurf's AI) for codebase understanding
- Follow agent contracts from `agents/*.agent.md`
- Execute orchestrator via terminal: `python3 scripts/orchestrate.py`
- Use Flow mode for multi-file implementations
```

### 3. Configure Windsurf Context

Create `.windsurfrules` in the repo root:

```markdown
# AI Agent Development Harness - Windsurf Rules

## Primary Context
Always read WINDSURF.md first for workspace structure and methodology.

## Agent-Driven Development
When asked to perform work:
1. Identify the agent role (Builder, Planner, Reviewer, Evaluator)
2. Read the corresponding agent contract from `agents/<role>.agent.md`
3. Follow the contract's scope, permissions, and output requirements

## Lifecycle Stages
Progress through stages in order:
1. Task Definition (stages/01-task-definition/)
2. Agent Design (stages/02-agent-design/)
3. Prompt Design (stages/03-prompt-design/)
4. Tool Integration (stages/04-tool-integration/)
5. Evaluation (stages/05-evaluation/)
6. Iteration (stages/06-iteration/)
7. Release (stages/07-release/)

Each stage has a CONTEXT.md with inputs, outputs, and procedures.

## Autonomy Modes (v1.2.0+)
Orchestrator supports 3 autonomy modes:
- `ask`: Manual approval for all operations
- `cautious`: Balanced (default) - auto LOW/MEDIUM, ask HIGH, block CRITICAL
- `full`: Auto-approve all (trusted automation)

Default to cautious mode unless user specifies otherwise.
```

## Windsurf-Specific Features

### Using Cascade (Windsurf's AI Agent)

Cascade is Windsurf's multi-agent AI system. Use it to work with the harness:

#### 1. **Codebase Understanding**

```
User: Explain how the autonomy system works

Cascade: I'll analyze the autonomy system across the codebase.
[Cascade automatically reads:]
- configs/autonomy.yaml
- scripts/orchestrator/autonomy_manager.py
- scripts/orchestrator/driver.py
- docs/AUTONOMY-MODES.md

The autonomy system has 3 modes...
```

Cascade automatically finds and reads relevant files without explicit @-mentions.

#### 2. **Multi-File Implementations**

```
User: Implement the deployment agent following the harness structure

Cascade: I'll create:
1. agents/deployer.agent.md - Agent contract
2. skills/deploy/deploy.md - Deployment skill
3. prompts/deployer/v1.md - Deployment prompt
4. Update configs/agents.yaml - Add deployer profile

[Shows multi-file changes in Flow mode]
```

### Flow Mode for Complex Changes

Windsurf's Flow mode is perfect for harness workflows:

```
User: /flow Implement Phase B of the autonomy system

Cascade (in Flow mode):
Understanding the task...
✓ Read stages/06-iteration/output/AUTOPLAN.md
✓ Identified files to modify: driver.py, orchestrate.py
✓ Planning changes across 2 files

Step 1/2: Integrate autonomy into driver.py
Step 2/2: Add CLI flag to orchestrate.py

[Shows interactive step-by-step implementation]
```

### Terminal Integration

Windsurf has excellent terminal integration:

```bash
# Access terminal: Ctrl+` (Windows/Linux) or Cmd+` (Mac)

# Run orchestrator
python3 scripts/orchestrate.py route iteration --execute --adapter cli --autonomy cautious

# Run tests
python3 -m pytest scripts/orchestrator/tests/ -v

# Validate harness
bash scripts/07-validate-harness.sh
```

## Orchestrator Configuration

### Option 1: Use Aider CLI Adapter (Recommended)

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
```

Install aider: `pip install aider-chat`

### Option 2: Manual Execution

Use dry-run mode and copy context to Cascade:

```bash
# Generate context bundles
python3 scripts/orchestrate.py route iteration

# Copy context from runs/*.md to Cascade chat
```

### Option 3: Custom Windsurf Adapter (Advanced)

Write a custom adapter that uses Codeium's API:

```python
# scripts/orchestrator/windsurf_adapter.py
from scripts.orchestrator.adapter import Adapter, StepResult

class WindsurfAdapter(Adapter):
    """Adapter for Windsurf/Codeium API."""

    name = "windsurf"

    def run(self, bundle, runs_dir, label):
        # Call Codeium API with bundle.render()
        # Return StepResult
        pass
```

## Adaptation Steps

### Step 1: Rename Claude-Specific Files

```bash
# Rename main configuration
mv CLAUDE.md WINDSURF.md

# Remove Claude Code-specific directory
rm -rf .claude/

# Update references
find docs -type f -name "*.md" -exec sed -i '' 's/Claude Code/Windsurf/g' {} +
find agents -type f -name "*.md" -exec sed -i '' 's/Claude Code/Windsurf/g' {} +
find skills -type f -name "*.md" -exec sed -i '' 's/Claude Code/Windsurf/g' {} +
```

### Step 2: Update Agent Contracts

**agents/builder.agent.md:**

```markdown
## Tools Allowed (Windsurf)

- Read files via Cascade's automatic context loading
- Search codebase using Windsurf's search (Cmd+Shift+F)
- Modify approved files using Flow mode
- Run validation commands in terminal
- Use Cascade for multi-file implementations

## Tools Disallowed

- Make unrelated changes
- Install dependencies without approval
- Run destructive commands without explicit approval
- Commit changes without explicit approval
```

### Step 3: Adapt Skills for Windsurf

**Before (Claude Code):**
```markdown
## Procedure

1. Use GitNexus MCP: `gitnexus_impact({target: "symbolName"})`
2. Read files with Read tool
3. Edit with Edit tool
```

**After (Windsurf):**
```markdown
## Procedure

1. Ask Cascade to find all references to the symbol
2. Review impact using Windsurf's "Find All References" (Shift+F12)
3. Edit files using Flow mode for multi-file changes
```

### Step 4: Configure Workspace Settings

Create `.vscode/settings.json` (Windsurf uses VS Code settings format):

```json
{
  "editor.formatOnSave": true,
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "scripts/orchestrator/tests"
  ],
  "files.exclude": {
    "**/.git": true,
    "**/__pycache__": true,
    "**/*.pyc": true,
    "runs/*.md": false
  },
  "search.exclude": {
    "runs/": true,
    ".venv/": true
  }
}
```

## Using the Harness in Windsurf

### Workflow 1: Agent-Driven Development (Recommended)

```
User: Act as the Planner agent and create a plan for adding rate limiting

Cascade: I'll read the Planner agent contract first.
[Automatically reads agents/planner.agent.md]

Based on the contract, my scope includes:
- Creating implementation-ready plans
- Defining validation criteria
- Identifying affected files

Let me create the plan...
[Creates output in stages/01-task-definition/output/]
```

### Workflow 2: Orchestrated Execution with Aider

```bash
# 1. Install aider
pip install aider-chat

# 2. Configure orchestrator
cat > configs/execution.yaml << 'EOF'
execution:
  default_adapter: cli
  cli:
    command: ["aider", "--yes", "--message"]
    timeout_seconds: 300
EOF

# 3. Run orchestrator
python3 scripts/orchestrate.py route iteration --execute --adapter cli --autonomy cautious

# 4. Review in Windsurf
# - Check runs/ for execution records
# - Review runs/autonomy-decisions.jsonl
# - Validate outputs
```

### Workflow 3: Manual Stage Progression

```
User: Let's start the iteration stage

Cascade: I'll guide you through stages/06-iteration/

[Reads stages/06-iteration/CONTEXT.md]

This stage requires:
Inputs:
- Eval results or review findings
- Original plan or implementation

Outputs:
- Iteration notes
- Updated implementation
- Revised validation results

Let's begin with step 1...
```

## Code Intelligence in Windsurf

Windsurf has excellent built-in code intelligence. Use these features:

### 1. Find References

```
Right-click on any symbol → "Find All References" (Shift+F12)
```

Alternative to GitNexus's `gitnexus_context()`.

### 2. Go to Definition

```
Cmd+Click (Mac) or Ctrl+Click (Windows) on any symbol
```

### 3. Symbol Search

```
Cmd+T (Mac) or Ctrl+T (Windows) - Go to Symbol in Workspace
```

### 4. Ask Cascade

```
User: Find all places where autonomy_mode is used

Cascade: I'll search the codebase for autonomy_mode references.
[Shows all usages with context]
```

### 5. Semantic Search

Windsurf's AI can do semantic code search:

```
User: Show me all functions that handle user authentication

Cascade: [Finds authentication-related functions even without exact keyword matches]
```

## Testing in Windsurf

### Using Windsurf's Test Runner

Windsurf supports pytest natively:

1. Open Test Explorer (sidebar icon)
2. Tests auto-discovered from `scripts/orchestrator/tests/`
3. Run individual tests or suites
4. View results inline

### Terminal Testing

```bash
# Run specific test file
python3 -m pytest scripts/orchestrator/tests/test_autonomy_manager.py -v

# Run all tests
python3 -m pytest scripts/orchestrator/tests/ -v

# Run with coverage
python3 -m pytest scripts/orchestrator/tests/ --cov=scripts/orchestrator --cov-report=html
```

## Best Practices for Windsurf

### 1. Leverage Cascade's Context Awareness

Cascade automatically understands your codebase. Don't over-specify:

```
❌ "Read agents/builder.agent.md, then read skills/build/build.md, then..."
✅ "Act as the Builder agent and implement this feature"
```

Cascade will automatically load the necessary context.

### 2. Use Flow Mode for Multi-Step Tasks

```
User: /flow Implement the complete autonomy system

Cascade (in Flow mode):
I'll break this into phases:
1. Core infrastructure
2. Integration
3. Documentation

Starting Phase 1...
```

Flow mode keeps context across multiple steps.

### 3. Create Custom Commands

Add to `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Orchestrator: Dry Run",
      "type": "shell",
      "command": "python3 scripts/orchestrate.py route ${input:routeName}",
      "problemMatcher": []
    },
    {
      "label": "Harness: Validate",
      "type": "shell",
      "command": "bash scripts/07-validate-harness.sh",
      "group": "test"
    },
    {
      "label": "Tests: Run All",
      "type": "shell",
      "command": "python3 -m pytest scripts/orchestrator/tests/ -v",
      "group": "test"
    }
  ],
  "inputs": [
    {
      "id": "routeName",
      "type": "pickString",
      "description": "Select route",
      "options": ["iteration", "release", "task_definition", "evaluation"],
      "default": "iteration"
    }
  ]
}
```

Run via Cmd+Shift+P → "Tasks: Run Task"

### 4. Use .windsurfrules for Consistent Behavior

Keep `.windsurfrules` updated with:
- Agent contract references
- Project conventions
- Common workflows
- Autonomy recommendations

### 5. Organize Workspace with Folders

Create a `.vscode/workspace.code-workspace` file:

```json
{
  "folders": [
    {
      "path": ".",
      "name": "Harness Root"
    },
    {
      "path": "agents",
      "name": "Agent Contracts"
    },
    {
      "path": "skills",
      "name": "Skills"
    },
    {
      "path": "stages",
      "name": "Lifecycle Stages"
    }
  ],
  "settings": {
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
  }
}
```

## Troubleshooting

### Issue: Cascade makes changes outside agent scope

**Solution:** Be explicit about agent boundaries:

```
User: As the Builder agent (see agents/builder.agent.md), implement only the core logic. Do not modify configs or documentation.
```

### Issue: Flow mode loses context

**Solution:** Reference previous steps explicitly:

```
User: Continue with Phase 2 (based on the Phase 1 changes you just made)
```

### Issue: Can't find certain files

**Solution:** Windsurf's search may exclude certain directories. Check `.vscode/settings.json`:

```json
{
  "search.exclude": {
    "runs/": false,  // Include runs in search
    ".venv/": true   // Exclude venv
  }
}
```

## Example Workflows

### Example 1: Create New Agent Contract

```
User: Create a new "Deployer" agent following the harness structure

Cascade: I'll create a new agent contract following the pattern from existing agents.

[Reads agents/builder.agent.md for structure]

Creating agents/deployer.agent.md with:
- Purpose
- Inputs
- Outputs
- Scope (IN SCOPE / OUT OF SCOPE)
- Tools Allowed/Disallowed
- Operating Rules
- Success Criteria
- Handoff

[Creates file with proper structure]

Also updating configs/agents.yaml to register the new agent...
```

### Example 2: Debug Orchestrator Issue

```
User: The orchestrator is failing on step 2. Help me debug.

Cascade: I'll check the orchestrator logs and code.

[Automatically reads:]
- runs/<latest-run-record>.md
- scripts/orchestrator/driver.py
- scripts/orchestrator/sequencer.py

I see the issue in driver.py line 152...
[Provides fix with explanation]
```

### Example 3: Run Complete Iteration Workflow

```bash
# Terminal workflow

# 1. Plan the iteration
python3 scripts/orchestrate.py route iteration

# 2. Review plan in Windsurf
# Open runs/<timestamp>-iteration-01-planner.md

# 3. Execute with aider
python3 scripts/orchestrate.py route iteration --execute --adapter cli --autonomy cautious

# 4. Use Cascade to review outputs
```

```
User in Windsurf: Review the iteration outputs for quality

Cascade: I'll check the outputs from the iteration route.
[Reads output files automatically]
[Provides quality assessment]
```

## Advanced: Windsurf + Orchestrator Integration

### Create Windsurf-Specific Adapter

```python
# scripts/orchestrator/windsurf_adapter.py
"""Windsurf/Codeium API adapter for orchestrator."""

import os
import requests
from scripts.orchestrator.adapter import Adapter, AdapterError, StepResult

class WindsurfAdapter(Adapter):
    """Execute steps via Windsurf/Codeium API."""

    name = "windsurf"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("CODEIUM_API_KEY")
        if not self.api_key:
            raise AdapterError("CODEIUM_API_KEY required for windsurf adapter")

    def run(self, bundle, runs_dir, label):
        """Send context to Codeium API, return result."""
        # Implementation would call Codeium's API
        # with bundle.render() as the prompt
        pass
```

Then configure:

```yaml
# configs/execution.yaml
execution:
  default_adapter: windsurf
  windsurf:
    api_key_env: CODEIUM_API_KEY
    timeout_seconds: 300
```

## Summary

**Windsurf Compatibility:**
- ✅ Excellent support for harness methodology
- ✅ Cascade AI understands agent contracts
- ✅ Flow mode perfect for multi-step workflows
- ✅ Strong code intelligence (alternative to GitNexus)
- ✅ Built-in test runner
- ✅ Excellent terminal integration

**Recommended Setup:**
1. Rename CLAUDE.md → WINDSURF.md
2. Create .windsurfrules with agent references
3. Remove .claude/ directory
4. Configure VS Code settings for Python/testing
5. Use aider for orchestrator execution (optional)
6. Leverage Cascade and Flow mode for implementations

**Effort:**
- Basic adaptation: 1-2 hours
- Full adaptation: 3-5 hours
- Learning curve: Low (intuitive AI interaction)

**Windsurf Advantages:**
- Superior context awareness (Cascade)
- Flow mode for complex multi-step tasks
- Native multi-file editing
- Strong semantic code understanding

Windsurf is an **excellent choice** for the harness due to its AI-native design, strong context management, and collaborative coding approach.
