# Harness Conventions and Naming Standards

This file documents the essential naming, formatting, and organizational conventions used throughout the harness.

## File Naming

### Date Prefixes
Use `YYYYMMDD` format for timestamped files:
- Run logs: `runs/20260616-143022-task_definition-01-researcher.md`
- Eval results: `evals/results/20260616-plan-quality-result.md`
- Never use: `MM-DD-YYYY`, `DD/MM/YY`, or other formats

### Slugification
Convert titles to lowercase-with-hyphens:
- Agent: `invoice-reviewer` not `Invoice_Reviewer` or `invoiceReviewer`
- Skill: `code-cleanup` not `codeCleanup`
- Plan: `native-orchestrator` not `Native Orchestrator`

## File Conventions

### Agent Files
- Contract: `agents/<agent-name>.agent.md`
- Example: `agents/planner.agent.md`, `agents/invoice-reviewer.agent.md`

### Skill Files
- Main procedure: `skills/<skill-name>/<skill-name>.md`
- Skill metadata: `skills/<skill-name>/SKILL.md`
- Example: `skills/plan/planner.md` + `skills/plan/SKILL.md`

### Prompt Versions
- Folder per prompt: `prompts/<prompt-name>/`
- Version files: `prompts/<prompt-name>/v1.md`, `v2.md`, etc.
- Changelog: `prompts/<prompt-name>/CHANGELOG.md`
- **Never overwrite versions; always increment**

### Stage Outputs
- Definition: `stages/<stage-number>-<stage-name>/output/<artifact>.md`
- Example: `stages/01-task-definition/output/task-definition.md`

## Load Indicators (Token Budgeting)

Stage CONTEXT.md files must specify how much of each file to load:

| Load Value | Meaning | Use When |
|------------|---------|----------|
| Full | Load entire file | Small files (<200 lines), critical context |
| Targeted | Load specific sections | Looking up a definition or contract |
| Relevant sections | Load sections matching task | Large reference files |
| Summary | Read title/purpose only | Orientation, checking existence |

## Commit Message Format

Follow conventional commit format:

```
<type>(<scope>): <subject>

[optional body]
```

**Types**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
**Scopes**: `agents`, `skills`, `prompts`, `configs`, `evals`, `stages`, `docs`

**Example**:
```
feat(agents): add invoice-reviewer agent with PCI detection

- Created agents/invoice-reviewer.agent.md
- Registered in configs/agents.yaml
- Added eval case for PCI field detection
```
