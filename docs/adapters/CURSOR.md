# Cursor Adaptation Guide

**Environment:** Cursor (VS Code-based AI IDE)
**Compatibility:** ✅ High (95% compatible)
**Effort:** 1-2 hours for basic setup, 4-6 hours for full adaptation

## Overview

Cursor is an excellent environment for the AI Agent Development Harness. It can read agent contracts, follow lifecycle stages, and execute the orchestrator. This guide covers how to adapt the harness for optimal Cursor usage.

## Quick Start (30 minutes)

### 1. Clone and Setup

```bash
# Clone the harness to your workspace
cd ~/projects
git clone <your-harness-repo>
cd th3rdai-harness

# Create Cursor-specific configuration
cp CLAUDE.md CURSOR.md
```

### 2. Update CURSOR.md

Replace the "Identity" section:

```markdown
# AI Agent Development Harness

## Identity

You are an AI assistant working inside an AI Agent Development Harness via Cursor. Your role is to help design, implement, evaluate, and improve reusable AI agents, prompts, skills, model profiles, and evaluation workflows.

## Environment: Cursor

This workspace uses Cursor's AI capabilities with the harness methodology:
- Use @-mentions to reference codebase context
- Follow agent contracts from `agents/*.agent.md`
- Execute orchestrator via terminal: `python3 scripts/orchestrate.py`
- Use Cursor's Composer for multi-file edits
```

### 3. Configure for Cursor Context

Create `.cursorrules` in the repo root:

```markdown
# AI Agent Development Harness - Cursor Rules

## Primary Instructions
Always read CURSOR.md first for workspace structure and methodology.

## Context Loading
- Check `agents/<role>.agent.md` before performing role-specific work
- Read `stages/<NN-stage>/CONTEXT.md` for stage-specific guidance
- Load only what you need from the framework layers

## Agent Contracts
When asked to act as:
- **Builder**: Read `agents/builder.agent.md` first
- **Planner**: Read `agents/planner.agent.md` first
- **Reviewer**: Read `agents/reviewer.agent.md` first
- **Evaluator**: Read `agents/evaluator.agent.md` first

## Workflow
1. Understand the task from user request
2. Load relevant agent contract
3. Follow the lifecycle stage (stages/XX-*)
4. Document outputs in the appropriate location
5. Run validation when complete

## Autonomy (v1.2.0+)
The orchestrator supports 3 autonomy modes:
- `--autonomy ask`: Approve all operations manually
- `--autonomy cautious`: Balanced (default)
- `--autonomy full`: Auto-approve all

Use cautious mode for most work, ask mode when learning.
```

## Cursor-Specific Features

### Using @-Mentions

Cursor's @-mention system replaces MCP servers for context:

| Task | Cursor Approach | Original (Claude Code) |
|------|----------------|------------------------|
| Search codebase | `@Codebase find authentication` | `mcp__gitnexus__query` |
| Reference files | `@Files agents/builder.agent.md` | Direct file read |
| Web search | `@Web latest Python best practices` | `WebSearch` tool |
| Documentation | `@Docs Python asyncio` | `WebFetch` tool |

**Example conversation:**

```
User: I need to add a new agent for deployment tasks

Cursor AI: Let me check the existing agent structure first.
@Files agents/builder.agent.md
@Files agents/planner.agent.md

Based on these contracts, I'll create a deployment agent...
```

### Using Composer for Multi-File Changes

When implementing features that touch multiple files:

```
User: Implement Phase A of the autonomy system plan

Cursor AI (in Composer mode):
I'll implement this across multiple files:
1. configs/autonomy.yaml - Configuration
2. scripts/orchestrator/autonomy_manager.py - Core logic
3. scripts/orchestrator/tests/test_autonomy_manager.py - Tests

[Cursor shows multi-file diff view]
```

### Terminal Integration

Cursor has excellent terminal integration for running the orchestrator:

```bash
# Run orchestrator from Cursor's terminal
# Ctrl+` to open terminal

# Dry run (see what would execute)
python3 scripts/orchestrate.py route iteration

# Execute with cautious autonomy
python3 scripts/orchestrate.py route iteration --execute --adapter cli --autonomy cautious
```

## Orchestrator Configuration

### Configure for Cursor's CLI

Create/update `configs/execution.yaml`:

```yaml
execution:
  default_adapter: cli
  cli:
    # Use Cursor's AI via command line
    command: ["npx", "cursor-cli", "--message"]
    timeout_seconds: 300
    env_allowlist:
      - PATH
      - HOME
      - CURSOR_API_KEY  # If using API mode
```

**Note:** Cursor doesn't have a native CLI yet. Options:

1. **Use Aider** (recommended): Install aider and configure the CLI adapter
2. **Manual execution**: Use dry-run mode, copy context to Cursor chat
3. **Custom wrapper**: Write a script that calls Cursor's API

## Adaptation Steps

### Step 1: Remove Claude Code-Specific Content

```bash
# Remove .claude directory (Claude Code-specific)
rm -rf .claude/

# Remove or rename Claude-specific files
mv CLAUDE.md CURSOR.md

# Update references in documentation
find docs -type f -name "*.md" -exec sed -i '' 's/Claude Code/Cursor/g' {} +
find agents -type f -name "*.md" -exec sed -i '' 's/Claude Code/Cursor/g' {} +
```

### Step 2: Update Agent Contracts

Edit each agent contract to reference Cursor features:

**agents/builder.agent.md:**

```markdown
## Tools Allowed (Cursor)

- Read files via @Files or direct file operations
- Search workspace via @Codebase
- Modify approved files using Cursor's editor
- Run validation commands in terminal
- Use Composer for multi-file changes
```

### Step 3: Adapt Skills

Update skill files to use Cursor's approach:

**Before (Claude Code):**
```markdown
## Procedure

1. Use GitNexus to find all callers: `gitnexus_impact({target: "symbolName"})`
2. Read source files with Read tool
```

**After (Cursor):**
```markdown
## Procedure

1. Use @Codebase to find references: `@Codebase find references to symbolName`
2. Read source files via @Files or direct file access
```

### Step 4: Configure Python Environment

Cursor works best when you configure your Python environment:

```bash
# Create .vscode/settings.json (Cursor uses VS Code settings)
mkdir -p .vscode
cat > .vscode/settings.json << 'EOF'
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "scripts/orchestrator/tests"
  ],
  "files.exclude": {
    "**/.git": true,
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
EOF
```

## Using the Harness in Cursor

### Manual Workflow (No Orchestrator)

**Best for learning and ad-hoc tasks:**

1. **Start a task:**
   ```
   User: I need to plan a new feature for user authentication

   Cursor AI: Let me load the planning agent contract and task definition stage.
   @Files agents/planner.agent.md
   @Files stages/01-task-definition/CONTEXT.md
   ```

2. **Follow stage guidance:**
   - Cursor reads the CONTEXT.md file
   - Follows the inputs/outputs/procedure
   - Creates outputs in the stage's output/ folder

3. **Validate:**
   ```bash
   # Run in Cursor's terminal
   bash scripts/07-validate-harness.sh
   ```

### Semi-Automated Workflow (With Orchestrator)

**Best for repeatable workflows:**

1. **Plan the route:**
   ```bash
   # See what steps would run
   python3 scripts/orchestrate.py route iteration
   ```

2. **Execute with aider adapter:**
   ```bash
   # Install aider first: pip install aider-chat

   # Configure execution.yaml for aider
   cat > configs/execution.yaml << 'EOF'
   execution:
     default_adapter: cli
     cli:
       command: ["aider", "--yes", "--message"]
       timeout_seconds: 300
       env_allowlist: ["PATH", "HOME"]
   EOF

   # Run with orchestrator
   python3 scripts/orchestrate.py route iteration --execute --adapter cli --autonomy cautious
   ```

3. **Review outputs in Cursor:**
   - Check `runs/` for execution records
   - Review `runs/autonomy-decisions.jsonl` for approval decisions
   - Validate outputs in stage folders

### Fully Manual Workflow (Pure Cursor)

**For maximum control:**

1. Ask Cursor to act as a specific agent:
   ```
   User: Act as the Builder agent and implement this plan

   Cursor AI: I'll read the Builder agent contract first.
   @Files agents/builder.agent.md

   Based on the contract, I understand my role is to...
   [Follows contract rules, permissions, outputs]
   ```

2. Use Cursor's Composer for multi-step implementations

3. Manually progress through lifecycle stages

## Code Intelligence Alternatives

Since Cursor doesn't have GitNexus MCP, use these alternatives:

### Option 1: Cursor's Built-in Search

```
@Codebase find all calls to validateUser
@Codebase find classes that implement AuthProvider
@Codebase show me the authentication flow
```

### Option 2: Install Language Server

Cursor supports LSP (Language Server Protocol) for code intelligence:

```json
// .vscode/settings.json
{
  "python.languageServer": "Pylance",
  "typescript.suggest.autoImports": true
}
```

### Option 3: Use Tree-sitter Queries

For advanced code queries, use tree-sitter via scripts:

```bash
# Install tree-sitter CLI
npm install -g tree-sitter-cli

# Query AST (you'd write query scripts)
tree-sitter query -q "(function_definition name: (identifier) @fn)" **/*.py
```

### Option 4: Integrate External Tools

Cursor's terminal can run any CLI tool:

```bash
# Use semgrep for pattern matching
semgrep --config auto --json src/

# Use sourcegraph CLI for code search
src search 'pattern:validateUser lang:python'

# Use ctags for symbol navigation
ctags -R . && grep validateUser tags
```

## Testing in Cursor

### Run Tests via Terminal

```bash
# Unit tests
python3 -m pytest scripts/orchestrator/tests/test_autonomy_manager.py -v

# All tests
python3 -m pytest scripts/orchestrator/tests/ -v

# Validation
bash scripts/07-validate-harness.sh
```

### Use Cursor's Test Explorer

Configure pytest in `.vscode/settings.json`:

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "scripts/orchestrator/tests"
  ],
  "python.testing.unittestEnabled": false
}
```

Then use Cursor's Test Explorer sidebar to run tests interactively.

## Best Practices for Cursor

### 1. Use .cursorrules for Project-Specific Guidance

Keep `.cursorrules` updated with:
- Agent contract references
- Common workflows
- Project-specific conventions
- Autonomy mode recommendations

### 2. Leverage Cursor's Chat History

Cursor remembers conversation context:
- Reference prior discussions
- Build on previous work
- Maintain context across sessions

### 3. Use Composer for Multi-File Edits

When implementing features that span multiple files, use Composer mode for:
- Consistent changes across files
- Preview all changes before applying
- Atomic commits

### 4. Configure Cursor Rules per Stage

Create stage-specific `.cursorrules` in each stage directory:

```markdown
# stages/01-task-definition/.cursorrules

When working in this stage:
1. Read CONTEXT.md first
2. Output to output/task-definition.md
3. Include scope boundaries
4. List open questions
```

### 5. Use Cursor's Command Palette

Add custom tasks to `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Harness: Validate",
      "type": "shell",
      "command": "bash scripts/07-validate-harness.sh",
      "group": "test"
    },
    {
      "label": "Harness: Dry Run Iteration",
      "type": "shell",
      "command": "python3 scripts/orchestrate.py route iteration",
      "group": "build"
    }
  ]
}
```

## Troubleshooting

### Issue: Cursor doesn't follow agent contracts

**Solution:** Be explicit in your requests:

```
❌ "Implement this feature"
✅ "Act as the Builder agent (see agents/builder.agent.md) and implement this feature"
```

### Issue: Context gets lost between messages

**Solution:** Use @Files to reload context:

```
User: Continue implementing the autonomy system

Cursor AI: @Files stages/06-iteration/output/AUTOPLAN.md
Let me review the plan first...
```

### Issue: Orchestrator can't execute in Cursor

**Solution:** Use one of these approaches:

1. **Manual execution:** Copy context bundles to Cursor chat
2. **Use aider:** Install aider and configure CLI adapter
3. **Dry-run mode:** Review what would execute, do it manually in Cursor

## Example Workflows

### Workflow 1: Create a New Feature (Manual)

```
User: I need to add a /health endpoint to the API

Cursor AI: I'll follow the harness methodology:

Step 1: Task Definition
@Files stages/01-task-definition/CONTEXT.md
Let me create a task definition...

Step 2: Planning
@Files agents/planner.agent.md
Based on the plan, I'll create an implementation plan...

Step 3: Implementation
@Files agents/builder.agent.md
Now I'll implement the feature...

Step 4: Validation
Let me run the tests...
```

### Workflow 2: Review Code Changes

```
User: Review this PR for the autonomy system

Cursor AI: I'll act as the Reviewer agent.
@Files agents/reviewer.agent.md

Based on the contract, I'll review for:
- Correctness against the plan
- Safety (no unintended changes)
- Maintainability
...
```

### Workflow 3: Run Orchestrator with Aider

```bash
# Terminal workflow

# 1. Configure aider adapter
cat > configs/execution.yaml << 'EOF'
execution:
  default_adapter: cli
  cli:
    command: ["aider", "--yes", "--message"]
    timeout_seconds: 300
EOF

# 2. Run iteration route
python3 scripts/orchestrate.py route iteration --execute --adapter cli --autonomy cautious

# 3. Review outputs in Cursor
# - Check runs/ for execution records
# - Review generated code
# - Run tests
```

## Summary

**Cursor Compatibility:**
- ✅ Excellent support for harness methodology
- ✅ Can read and follow agent contracts
- ✅ Terminal integration for orchestrator
- ✅ Multi-file editing with Composer
- ✅ Built-in code intelligence (alternative to GitNexus)

**Recommended Setup:**
1. Rename CLAUDE.md → CURSOR.md
2. Create .cursorrules with agent contract references
3. Remove .claude/ directory
4. Configure VS Code settings for Python
5. Use aider for orchestrator execution (optional)

**Effort:**
- Basic adaptation: 1-2 hours
- Full adaptation: 4-6 hours
- Learning curve: Minimal (Cursor is intuitive)

Cursor is one of the **best environments** for the harness due to its VS Code foundation, excellent AI integration, and strong terminal support.
