# Contributing

This repository is a plain-text, model-agnostic AI agent/model development harness. Contributions should preserve its core principle: **explicit, inspectable contracts over implied behavior.**

## Before You Start

1. Read `README.md`, `FRAMEWORK.md`, and `GLOSSARY.md`.
2. Use `CONTEXT.md` to route your change to the right lifecycle stage.
3. Read the relevant agent contract in `agents/` and any related skill.

## Workflow

Follow the harness lifecycle for any non-trivial change:

```text
Task Definition → Agent Design → Prompt Design → Tool Integration → Evaluation → Iteration → Release
```

A typical change:

1. `/research` — gather grounded context.
2. `/plan` — produce an implementation-ready plan.
3. `/plan-reviewer` — review the plan.
4. `/build` — implement within approved scope.
5. `/validate` and `/eval` — confirm structure and behavior.
6. `/gitcommit` — prepare a reviewed commit (Stage 07).

## Conventions

- **Agents** live in `agents/<name>.agent.md`. Keep role, permissions, inputs, outputs, and handoffs explicit.
- **Skills** use the two-file pattern: `skills/<name>/SKILL.md` (summary + Procedure link) and `skills/<name>/<name>.md` (executable procedure). Wire the skill to its agent in `configs/agents.yaml`.
- **Prompts** are versioned: never overwrite a version; add `vN.md` and record the reason in the prompt's `changelog.md`. Register it in `prompts/registry.md`.
- **Configs** are machine-readable. Any path referenced in `configs/agents.yaml`, `configs/routing.yaml`, or `prompts/registry.md` must resolve.
- **Evals** are first-class. New behavior should have a rubric and/or case, and results recorded in `evals/results/` and `runs/`.

## Validation

Run structural and cross-reference validation before opening a PR:

```bash
bash -n scripts/*.sh
scripts/07-validate-harness.sh
```

The validation script verifies required structure **and** that config/registry cross-references resolve. It must pass with zero failures.

## Safety

Per `configs/tools.yaml` and `CLAUDE.md`:

- Do not install dependencies, run destructive commands, or commit without explicit approval.
- Do not read secrets unless required and approved.
- Keep destructive or irreversible actions behind human review.
- Prefer read-only network, MCP, and browser access; escalate before any write or authenticated action.

## Pull Requests

- Keep changes small and reviewable.
- Describe which harness layer(s) changed and why.
- Note validation results and any skipped checks honestly.
- Update `GLOSSARY.md`, `prompts/registry.md`, or `runs/README.md` when you add agents, skills, prompts, or notable runs.
