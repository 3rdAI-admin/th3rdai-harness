# Quick Reference Guide

Fast lookup for common harness operations and navigation patterns.

## 5-Layer Navigation Model

The harness uses a **5-layer progressive disclosure** system:

| Layer | File | Purpose | When to Read |
|-------|------|---------|--------------|
| **1. Entry** | `CLAUDE.md` | Identity, rules, folder map | Every session start |
| **2. Routing** | `CONTEXT.md` | Stage selector, current focus | When starting new work |
| **3. Stage** | `stages/<stage>/CONTEXT.md` | Stage contract, required files | At stage entry |
| **4. Agent** | `agents/<agent>.agent.md` | Agent role, inputs/outputs | Before invoking agent |
| **5. Implementation** | Prompts, configs, skills | Execution details | During task execution |

**Never skip layers** — each provides context needed for the next.

## Common Commands

### Validation
```bash
scripts/07-validate-harness.sh              # Full harness validation
python3 -m unittest discover scripts/orchestrator/tests  # Orchestrator tests
```

### Orchestrator (when implemented)
```bash
python3 scripts/orchestrate.py route <name> --dry-run    # Preview execution
python3 scripts/orchestrate.py route <name> --execute    # Execute with CLI
python3 scripts/orchestrate.py eval <case.md>            # Run eval case
```

### Bootstrap New Project
```bash
scripts/01-create-project.sh                      # Interactive
scripts/01-create-project.sh --with-orchestrator  # Include orchestrator CLI
HARNESS_PROJECT_PATH=/path HARNESS_OVERWRITE=1 scripts/01-create-project.sh  # Non-interactive
```

## File Naming Standards

**See `_config/conventions.md` for full details.**

| Pattern | Example | Never Use |
|---------|---------|-----------|
| Dates | `20260616-143022-task.md` | `06-16-2026`, `16/06/26` |
| Slugs | `invoice-reviewer` | `Invoice_Reviewer`, `invoiceReviewer` |
| Agent | `agents/<name>.agent.md` | `agents/<name>.md` |
| Skill | `skills/<name>/<name>.md` + `SKILL.md` | `skills/<name>.md` |
| Prompt | `prompts/<name>/v1.md` (never overwrite) | `prompts/<name>.md` |

## Lifecycle Stages

| Stage | Purpose | Key Files |
|-------|---------|-----------|
| **01 Task Definition** | Understand the problem | `INITIAL.md`, `task-definition.md` |
| **02 Agent Design** | Design agent roles | `agent-contract.md` |
| **03 Prompt Design** | Write prompts | `v1.md`, `CHANGELOG.md` |
| **04 Tool Integration** | Connect tools | `tool-profile.md` |
| **05 Evaluation** | Test and score | rubric + case + result |
| **06 Iteration** | Improve based on eval | `iteration-plan.md` |
| **07 Release** | Production-ready | `release-checklist.md` |

## Agent Contracts Quick Lookup

| Agent | Role | Inputs | Outputs |
|-------|------|--------|---------|
| **Researcher** | Understand problem | Task description | Research findings |
| **Planner** | Design solution | Research findings | Implementation plan |
| **Builder** | Implement | Plan + context | Working code/config |
| **Reviewer** | Quality check | Builder output | Review report |
| **Evaluator** | Score against rubric | Output + rubric | Scored result |

## Eval Workflow

1. **Define rubric** → `evals/rubrics/<name>.md`
2. **Create case** → `evals/cases/<category>/<case>.md` (reference rubric)
3. **Run evaluation** → manual or via orchestrator
4. **Record result** → `evals/results/YYYYMMDD-<name>-result.md`

## Common Pitfalls

| ❌ Don't | ✅ Do |
|---------|-------|
| Edit prompt versions | Create new version (v2, v3) |
| Skip stage CONTEXT.md | Read contract first |
| Hardcode paths in skills | Use `$PROJECT_ROOT`, `_config/project-notes.md` |
| Guess file locations | Check folder map in CLAUDE.md |
| Create files without eval | Write rubric + case first |

## Load Indicators (Token Budgeting)

When stage CONTEXT.md specifies how much to load:

| Indicator | Load | Use When |
|-----------|------|----------|
| **Full** | Entire file | Small critical files (<200 lines) |
| **Targeted** | Specific sections | Looking up definitions |
| **Relevant sections** | Sections matching task | Large reference files |
| **Summary** | Title/purpose only | Orientation phase |

## Need Help?

| Question | Read This |
|----------|-----------|
| What is this harness? | `README.md` → `FRAMEWORK.md` |
| How do I start? | `TUTORIAL.md` |
| Where do I add X? | `CLAUDE.md` folder map |
| What are the rules? | `_config/conventions.md` |
| How do I distribute? | `DISTRIBUTION.md` |
| Current status? | `VERSION3.md` |
