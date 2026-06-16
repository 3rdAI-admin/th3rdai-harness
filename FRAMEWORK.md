# AI Agent Development Harness

## Purpose

This repository is a plain-text, model-agnostic harness for designing, evaluating, and improving AI agents and model workflows.

The harness uses structured context, reusable skills, versioned prompts, explicit agent contracts, model profiles, and evaluation rubrics so AI-assisted work can be repeated, inspected, and improved over time.

## Operating Model

The harness is **agent-driven, not engine-driven** by default: "agents" are role contracts and "skills" are procedures a capable AI agent (or human) follows. Routing (`configs/routing.yaml`) and stage contracts describe the intended sequence. An optional **Native Orchestrator** (`scripts/orchestrate.py`, `plans/native-orchestrator/`) automates sequencing, context-bundle assembly, and run logging — dry-run by default, with opt-in `--execute` via `configs/execution.yaml`. The core stays dependency-free (Python stdlib only).

## 5-Layer Navigation Model

The harness uses a **5-layer navigation model** to help you load context progressively. Think of it like an employee handbook: you don't read every page on day one — you consult different sections based on your current question.

### The Five Layers

```text
┌─────────────────────────────────────────────────┐
│ Layer 1: ORIENTATION (CLAUDE.md, CONTEXT.md)  │
│ "Where am I? What's my role? Where do I start?"│
│ ~1,200 tokens                                   │
└─────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────┐
│ Layer 2: FOUNDATION (FRAMEWORK.md, agents/)    │
│ "What are the concepts? Who does what?"         │
│ ~2,000-3,000 tokens (targeted)                  │
└─────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────┐
│ Layer 3: DOMAIN (skills/, prompts/, models/)   │
│ "How do I perform this specific task?"          │
│ ~1,000-2,000 tokens (single skill/prompt)       │
└─────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────┐
│ Layer 4: EXECUTION (stages/, configs/, evals/)│
│ "What's the step-by-step process for this stage?"│
│ ~1,500-3,000 tokens (single stage)              │
└─────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────┐
│ Layer 5: CONTINUITY (runs/, telemetry/, plans/)│
│ "What happened? What's the history? What's next?"│
│ ~1,000-5,000 tokens (targeted runs/plans)       │
└─────────────────────────────────────────────────┘
```

### Navigation Guide

| Question | Start Here | Estimated Tokens |
|----------|-----------|------------------|
| "What is this workspace?" | CLAUDE.md + CONTEXT.md | ~1,200 |
| "How do agents work?" | FRAMEWORK.md (Foundation section) | ~600 |
| "How do I create a plan?" | skills/plan/planner.md | ~1,500 |
| "What's the task definition process?" | stages/01-task-definition/CONTEXT.md | ~350 |
| "What did we try before?" | runs/ (targeted) | Variable |

### Token Budget Best Practices

**AI assistants**: Load context progressively. Each stage CONTEXT.md specifies exactly which files to load and how much (see Load column).

**Rule**: Trust the Load indicators in stage contracts. Don't load entire files when "Relevant sections" is specified.

**Token Calculation**: Files measured as `words × 1.3 = tokens`. Budget estimates include ±20% margin.

## Core Concepts

### Agent

An agent is an actor with a role, permissions, inputs, outputs, success criteria, and handoff rules.

Agents answer the question: **who is doing the work?**

Examples:

- Planner Agent
- Builder Agent
- Reviewer Agent
- Evaluator Agent
- Researcher Agent

### Skill

A skill is a reusable procedure an agent can follow.

Skills answer the question: **how should this work be done?**

Examples:

- `/plan`
- `/build`
- `/validate`
- `/security`
- `/code-cleanup`
- `/tests/e2e-test.md`
- `/gitcommit`

### Prompt

A prompt is a versioned instruction template used by an agent or skill.

Prompts answer the question: **what exact instruction pattern is being tested or reused?**

### Model Profile

A model profile describes which model/provider settings should be used for a task or agent.

Model profiles answer the question: **which model should perform this work and under what settings?**

### Evaluation

An evaluation is a repeatable test, rubric, or benchmark used to measure agent/model performance.

Evaluations answer the question: **how do we know the agent or model performed well?**

### Run

A run is a recorded execution of an agent, skill, prompt, or evaluation.

Runs answer the question: **what happened, with which inputs, model, outputs, and results?**

## Repository Layers

| Layer | Folder | Purpose |
|-------|--------|---------|
| Orientation | `CLAUDE.md`, `CONTEXT.md` | Tell AI assistants how to operate in this workspace |
| Framework | `FRAMEWORK.md` | Define the conceptual model and operating principles |
| Agents | `agents/` | Define roles, permissions, outputs, and handoffs |
| Skills | `skills/` | Store reusable workflows and command procedures |
| Prompts | `prompts/` | Version and track prompt templates |
| Plans | `plans/` | Store implementation-ready plans and multi-phase efforts |
| Models | `models/` | Document provider/model choices and tradeoffs |
| Configs | `configs/` | Store machine-readable agent/model/routing/tool profiles |
| Evals | `evals/` | Store rubrics, test cases, and evaluation results |
| Stages | `stages/` | Organize lifecycle work from task definition through release |
| Runs | `runs/` | Store execution records and experiment notes |
| Telemetry | `telemetry/` | Define logging and observability conventions |
| Scripts | `scripts/` | Bootstrap, validate, and maintain harness workspaces (see `DISTRIBUTION.md`) |
| Deployment overlay | `_config/project-notes.md` | Optional per-project commands, verify steps, and tooling pointers (see below) |

## Deployment overlay (optional)

Skills under `skills/` stay **portable**: they describe harness workflows without hardcoding paths, test counts, or CLIs that belong to one application.

When a bootstrapped project needs local detail (verify commands, optional subsystems, resume pointers, tracker IDs), maintain **`_config/project-notes.md`**. Copy from `_config/project-notes.TEMPLATE.md` during bootstrap (`skills/new-project.md`).

For web application security baseline regression (WASA/threat-model P0/P1/P2), maintain **`_config/security-baseline.md`**. Copy from `_config/security-baseline.TEMPLATE.md`. Use the portable `/security` skill for diff review and threat modeling; add an optional `skills/security-<project>/` overlay for `wasa` mode against your assessment doc.

Skill procedures may instruct agents to read `project-notes.md` when it exists. Keep deployment-specific content there — not duplicated inside portable skill files.

## Default Lifecycle

```text
Task Definition → Agent Design → Prompt Design → Tool Integration → Evaluation → Iteration → Release
```

Use the lifecycle when developing or improving an agent/model workflow:

1. Define the task, success criteria, and constraints.
2. Select or design the responsible agent.
3. Select or revise the prompt/skill used by the agent.
4. Define required tools, permissions, and safety boundaries.
5. Evaluate outputs with rubrics and test cases.
6. Iterate based on findings.
7. Release the updated agent, prompt, skill, or configuration.

## Design Principles

- Keep context inspectable and plain-text first.
- Prefer explicit contracts over implied behavior.
- Separate agents, skills, prompts, models, and evals.
- Record assumptions, inputs, outputs, and validation results.
- Treat evals as first-class artifacts, not optional documentation.
- Make tool permissions and destructive actions explicit.
- Preserve human review checkpoints for risky or irreversible actions.

## Minimum Definition of Done

A new or revised agent/model workflow is complete when:

- The agent contract exists or has been updated.
- The relevant skill or prompt is versioned and documented.
- Model/provider assumptions are recorded.
- Tool permissions and safety constraints are explicit.
- Evaluation criteria are defined.
- At least one representative test case or rubric has been run or documented.
- Follow-up risks and open questions are recorded.
