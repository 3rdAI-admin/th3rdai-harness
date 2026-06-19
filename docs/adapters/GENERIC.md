# Generic Environment Adaptation Guide

**For:** Any AI coding environment not covered by specific guides
**Compatibility:** Varies (60-95% depending on environment capabilities)
**Effort:** 2-6 hours depending on environment features

## Overview

This guide helps you adapt the AI Agent Development Harness for any AI coding environment, IDE, or LLM interface. The harness is fundamentally tool-agnostic and can work with any system that can:

1. Read markdown documentation
2. Follow instructions
3. Create and modify files
4. (Optional) Execute shell commands

## Compatibility Matrix

Assess your environment's capabilities:

| Capability | Required? | Impact if Missing |
|------------|-----------|-------------------|
| Read files | ✅ Required | Cannot use harness |
| Write files | ✅ Required | Cannot use harness |
| Follow markdown instructions | ✅ Required | Low effectiveness |
| Execute shell commands | ⚠️ Recommended | Cannot use orchestrator |
| Git operations | ⚠️ Recommended | Manual commits needed |
| Codebase search | ⚠️ Recommended | Slower context loading |
| Multi-file editing | ⚠️ Nice to have | More manual work |
| Context persistence | ⚠️ Nice to have | Repeat context loading |

## Quick Assessment

**Your environment is a good fit if it can:**

```
✅ Load and read: agents/builder.agent.md
✅ Understand the instructions in it
✅ Create a new file based on those instructions
✅ Follow a multi-step procedure from a CONTEXT.md file
```

**Test it:**

```
Prompt: "Read agents/builder.agent.md and explain what the Builder agent's responsibilities are."

Expected: Your AI should read the file and explain the agent's role, scope, permissions, etc.
```

## Basic Adaptation (2-3 hours)

### Step 1: Rename Environment-Specific Files

```bash
# Rename CLAUDE.md to match your environment
mv CLAUDE.md YOUR-ENV.md

# Update the identity section
# Example for "SuperCoder IDE":
```

```markdown
# AI Agent Development Harness

## Identity

You are an AI assistant working inside an AI Agent Development Harness via SuperCoder IDE. Your role is to help design, implement, evaluate, and improve reusable AI agents, prompts, skills, model profiles, and evaluation workflows.

## Environment: SuperCoder IDE

This workspace uses SuperCoder's AI capabilities with the harness methodology:
- Load agent contracts from `agents/*.agent.md` before acting
- Follow lifecycle stages in `stages/XX-*/`
- Use the framework layers (agents, skills, prompts, models, evals)
- Document outputs in appropriate stage folders

## How to Work

1. **Start here** — read this file to understand the workspace
2. **Read FRAMEWORK.md** to understand agents, skills, prompts, models, evals, and runs
3. **Check CONTEXT.md** in the root for routing to the right stage
4. **Read relevant agent contracts** before performing agent-specific work
5. **Load only what you need** — each stage tells you exactly which files to read
6. **Save outputs** to the relevant stage, eval, prompt, config, or run location
```

### Step 2: Update References

```bash
# Update all references to Claude Code
find . -type f -name "*.md" \
  -not -path "./.git/*" \
  -not -path "./.*" \
  -exec sed -i '' 's/Claude Code/SuperCoder/g' {} +

# Or manually search and replace in your environment
```

### Step 3: Remove Environment-Specific Directories

```bash
# Remove .claude/ if it exists (Claude Code-specific)
rm -rf .claude/

# Remove any other tool-specific directories
rm -rf .cursor/ .windsurf/ etc.
```

### Step 4: Test Basic Functionality

```
Prompt your AI:

"Act as the Planner agent (see agents/planner.agent.md) and create a simple plan for adding a health check endpoint to an API. Save the plan to stages/06-iteration/output/test-plan.md"

Expected behavior:
1. AI reads agents/planner.agent.md
2. Understands the Planner role and constraints
3. Creates a plan following the structure
4. Saves to the correct location
```

If this works, your environment is compatible! ✅

## Advanced Adaptation (4-6 hours)

### Adapting Agent Contracts

Edit agent contracts to reference your environment's specific features:

**Template for agents/*.agent.md:**

```markdown
## Tools Allowed (YourEnvironment)

- Read files via [YourEnv's file reading feature]
- Search codebase using [YourEnv's search feature]
- Modify approved files using [YourEnv's editing feature]
- Run validation commands [if terminal access available]

## Tools Disallowed

- Make unrelated changes
- Install dependencies without approval
- Run destructive commands without explicit approval
- Commit changes without explicit approval

## Environment-Specific Notes

[Add notes about how to use your environment's features effectively]
```

### Adapting Skills

Skills may reference tools not available in your environment. Update them:

**Before (Claude Code-specific):**

```markdown
## Procedure

1. Use GitNexus MCP: `gitnexus_impact({target: "symbolName"})`
2. Run with Read tool
3. Edit with Edit tool
```

**After (Generic):**

```markdown
## Procedure

1. Use [YourEnv's code search]: Search for all references to `symbolName`
2. Read the relevant files
3. Analyze impact manually or use [YourEnv's refactoring tools]
4. Make edits carefully
```

### Creating Environment-Specific Instructions

Create a file at `_config/YOUR-ENV-notes.md`:

```markdown
# SuperCoder IDE Notes

## How to Use Harness Features in SuperCoder

### Loading Agent Contracts
```
Ask AI: "Load and read agents/builder.agent.md"
```

### Following Stage Procedures
```
Ask AI: "Read stages/01-task-definition/CONTEXT.md and follow the procedure to create a task definition"
```

### Running Orchestrator
SuperCoder has no terminal access. Use manual workflow instead.
See Manual Workflow section below.

### Code Intelligence
Use SuperCoder's "Find References" feature instead of GitNexus.
```

## Orchestrator Integration Options

The orchestrator is the harness's automation layer. Here are options based on your environment's capabilities:

### Option 1: Full Integration (Terminal Access)

**If your environment has terminal/shell access:**

```yaml
# configs/execution.yaml
execution:
  default_adapter: cli
  cli:
    # Replace with your environment's CLI command
    command: ["your-ai-cli", "--message"]
    timeout_seconds: 300
    env_allowlist:
      - PATH
      - HOME
      - YOUR_API_KEY
```

```bash
# Test orchestrator
python3 scripts/orchestrate.py route iteration --execute --adapter cli
```

### Option 2: API Integration (Custom Adapter)

**If your environment has an API:**

Create a custom adapter:

```python
# scripts/orchestrator/your_adapter.py
from scripts.orchestrator.adapter import Adapter, StepResult

class YourEnvAdapter(Adapter):
    """Adapter for YourEnvironment API."""

    name = "yourenv"

    def __init__(self, api_key: str):
        self.api_key = api_key
        # Initialize API client

    def run(self, bundle, runs_dir, label):
        """Execute step via YourEnvironment API."""
        # Call API with bundle.render() as input
        response = your_api_client.send_message(bundle.render())

        # Parse response and return StepResult
        return StepResult(
            status="executed",
            outputs=["output/result.md"],
            tool_actions=["API call completed"],
            notes="Executed via YourEnvironment API"
        )
```

Then configure:

```yaml
# configs/execution.yaml
execution:
  default_adapter: yourenv
  yourenv:
    api_key_env: YOUR_ENV_API_KEY
```

### Option 3: Manual Workflow (No Automation)

**If your environment cannot run the orchestrator:**

Use the harness methodology manually:

1. **Read the routing:**
   ```
   Ask AI: "Read configs/routing.yaml and explain the 'iteration' route"
   ```

2. **Follow steps manually:**
   ```
   Ask AI: "Act as the Planner agent and execute step 1 of the iteration route"
   ```

3. **Progress through stages:**
   - Task Definition (stages/01-task-definition/)
   - Planning (stages/06-iteration/)
   - Implementation
   - Validation
   - Release (stages/07-release/)

4. **Record results:**
   Manually create run records in `runs/` following `telemetry/run-log-schema.md`

## Code Intelligence Alternatives

If your environment doesn't have GitNexus-like features:

### Option 1: Built-in IDE Features

Most IDEs have:
- Find All References (Shift+F12 or similar)
- Go to Definition
- Symbol Search
- Call Hierarchy

Use these instead of GitNexus MCP tools.

### Option 2: External CLI Tools

Install code intelligence tools and run from terminal:

```bash
# Universal ctags
ctags -R .
grep "symbol_name" tags

# Ripgrep for fast search
rg "pattern" --type py

# Tree-sitter for AST queries
tree-sitter query ...

# Semgrep for pattern matching
semgrep --config auto .
```

### Option 3: Ask AI to Search

```
Prompt: "Search the codebase for all calls to validateUser() and list the files and line numbers"
```

Most modern AI coding assistants can do semantic code search.

### Option 4: Language Server Protocol (LSP)

If your environment supports LSP:

```json
// .vscode/settings.json or equivalent
{
  "python.languageServer": "Pylance",
  "typescript.suggest.autoImports": true
}
```

LSP provides:
- Go to definition
- Find references
- Hover information
- Code completion

## Testing and Validation

### If Terminal Access Available:

```bash
# Run harness validation
bash scripts/07-validate-harness.sh

# Run orchestrator tests
python3 -m pytest scripts/orchestrator/tests/ -v
```

### If No Terminal Access:

Ask your AI to validate manually:

```
Prompt: "Check that all files referenced in configs/routing.yaml actually exist. List any missing files."
```

```
Prompt: "Verify that each agent in configs/agents.yaml has a corresponding contract file in agents/"
```

## Environment-Specific Workflows

### Workflow Template

Adapt this template for your environment:

```markdown
# YourEnvironment Workflow: Create New Feature

## Step 1: Task Definition
1. Open stages/01-task-definition/CONTEXT.md
2. Read the inputs, outputs, and procedure
3. Ask AI: "Act as the Researcher agent and create a task definition for [feature]"
4. Review output in stages/01-task-definition/output/

## Step 2: Planning
1. Open stages/06-iteration/CONTEXT.md
2. Ask AI: "Act as the Planner agent and create an implementation plan based on the task definition"
3. Review plan in stages/06-iteration/output/

## Step 3: Implementation
1. Open stages/06-iteration/CONTEXT.md
2. Ask AI: "Act as the Builder agent and implement the plan"
3. Review code changes

## Step 4: Validation
[If terminal access:]
   bash scripts/07-validate-harness.sh
[If no terminal:]
   Ask AI: "Review the implementation against the plan and validation criteria"

## Step 5: Release
1. Open stages/07-release/CONTEXT.md
2. Ask AI: "Act as the Reviewer agent and prepare this for release"
3. Review release notes
4. Commit changes [via your environment's git integration]
```

## Common Adaptation Challenges

### Challenge 1: AI Doesn't Follow Agent Contracts

**Solution:** Be explicit in your prompts:

```
❌ "Implement this feature"
✅ "Act as the Builder agent. First read agents/builder.agent.md to understand your role, then implement this feature following all constraints in the contract."
```

### Challenge 2: Context Gets Lost

**Solution:** Reference prior context explicitly:

```
"Based on the plan you created in stages/06-iteration/output/AUTOPLAN.md, continue with Phase 2..."
```

### Challenge 3: AI Makes Unrelated Changes

**Solution:** Use agent contract scope:

```
"Act as the Builder agent. You are IN SCOPE for implementation, OUT OF SCOPE for changing configs. Only modify the implementation files."
```

### Challenge 4: Can't Run Orchestrator

**Solution:** Use dry-run mode to see what would execute:

```bash
python3 scripts/orchestrate.py route iteration

# Copy the context bundles to your AI chat
# Execute steps manually
```

### Challenge 5: No Git Integration

**Solution:** Manual git workflow:

```bash
# In terminal (if available) or external terminal:
git status
git add [files]
git commit -m "feat: implemented feature X"
git push
```

## Measuring Compatibility

Score your environment (out of 100):

| Feature | Points | Your Score |
|---------|--------|------------|
| Reads markdown files | 20 | |
| Writes/edits files | 20 | |
| Follows multi-step instructions | 15 | |
| Terminal/shell access | 15 | |
| Codebase search | 10 | |
| Git operations | 10 | |
| Multi-file editing | 5 | |
| Context persistence | 5 | |

**Interpretation:**
- **90-100:** Excellent fit, minimal adaptation needed
- **75-89:** Good fit, 2-3 hours adaptation
- **60-74:** Moderate fit, 4-6 hours adaptation
- **Below 60:** Consider using a different environment or manual workflow only

## Example Adaptations

### GitHub Copilot Chat (VS Code)

**Score:** 70/100

```markdown
# COPILOT.md

Use with Copilot Chat in VS Code:
- Ask Copilot to read agent contracts
- Use @workspace to reference files
- Manual git workflow
- Cannot use orchestrator (no CLI integration)
- Good for manual stage progression
```

### Tabnine

**Score:** 50/100

```markdown
# TABNINE.md

Limited to autocomplete:
- Cannot read full documentation
- Cannot follow multi-step procedures
- Use harness as reference only
- Manual implementation of all stages
```

### Custom LLM API (Python Script)

**Score:** 95/100

```python
# custom_harness.py
import anthropic

client = anthropic.Anthropic(api_key="...")

def execute_step(step_context):
    """Execute a harness step via API."""
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{
            "role": "user",
            "content": step_context
        }]
    )
    return response.content
```

Excellent compatibility - can implement full orchestrator integration.

## Best Practices for Any Environment

### 1. Start with Agent Contracts

Always load the agent contract before asking your AI to act:

```
"Read agents/builder.agent.md. What is the Builder agent allowed and not allowed to do?"
```

### 2. Use Stage CONTEXT.md Files

Each stage has a CONTEXT.md with exact inputs, outputs, and procedures:

```
"Read stages/01-task-definition/CONTEXT.md and follow the procedure"
```

### 3. Keep Outputs Organized

Follow the harness directory structure:

```
stages/XX-stage/output/      # Stage outputs
runs/                        # Execution records
evals/results/               # Evaluation results
```

### 4. Validate Frequently

Check your work against:
- Agent contract constraints
- Stage success criteria
- Eval rubrics

### 5. Document Your Adaptation

Create `_config/YOUR-ENV-notes.md` with:
- How to use harness features in your environment
- Workarounds for missing capabilities
- Environment-specific tips

## Summary Template

After adapting, document your setup:

```markdown
# [YourEnvironment] Harness Setup

**Compatibility:** XX/100
**Adaptation Effort:** X hours
**Best For:** [Use cases]

## What Works
- ✅ [Feature 1]
- ✅ [Feature 2]

## What Doesn't Work
- ❌ [Missing feature 1]
- ❌ [Missing feature 2]

## Workarounds
- [Missing feature 1]: [How to work around it]

## Recommended Workflow
1. [Step 1]
2. [Step 2]
...

## Configuration
[Environment-specific config]
```

## Getting Help

If you're adapting for a specific environment and need help:

1. Check existing adapters: `docs/adapters/` for similar environments
2. Review harness structure: `FRAMEWORK.md` for core concepts
3. Test with simple tasks first
4. Document what works and what doesn't

The harness is designed to be flexible. If your environment can read markdown and follow instructions, you can make it work! 🚀
