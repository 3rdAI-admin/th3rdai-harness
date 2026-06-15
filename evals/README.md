# Evaluations

Evaluations measure whether agents, prompts, skills, and model profiles perform well enough to use or release.

Use this folder for repeatable rubrics, test cases, and results.

## Evaluation Flow

1. Select the agent, prompt, skill, and model profile.
2. Select a representative eval case.
3. Apply the relevant rubric without changing it mid-run.
4. Record the run inputs, outputs, scores, and findings.
5. Recommend revisions or release.

## Folder Map

| Folder | Purpose |
|--------|---------|
| `rubrics/` | Scoring criteria |
| `cases/` | Representative tasks and expected qualities |
| `results/` | Evaluation outputs and run summaries |

## Registered Rubrics

| Rubric | Scores |
|--------|--------|
| `rubrics/plan-quality.md` | Implementation-ready plans |
| `rubrics/agent-output-quality.md` | General agent output |
| `rubrics/tool-safety.md` | Tool-use safety and approval gating |
| `rubrics/orchestrator-output-quality.md` | Native-orchestrator artifacts (config parses, context bundles, run records) |

## Registered Cases

| Case | Rubric |
|------|--------|
| `cases/planning/basic-feature-plan.md` | `plan-quality` |
| `cases/prompt-design/prompt-revision.md` | `agent-output-quality` |
| `cases/code-review/security-bug-review.md` | `agent-output-quality` — procedure: `skills/security/security.md` (`/security`; portable) |
| `cases/agent-handoff/planner-to-builder.md` | `agent-output-quality` |
| `cases/debugging/failing-test-diagnosis.md` | `agent-output-quality` + `plan-quality` |
| `cases/tool-safety/destructive-command-request.md` | `tool-safety` |
| `cases/orchestrator/config-subset-parsing.md` | `orchestrator-output-quality` |
| `cases/orchestrator/run-record-fidelity.md` | `orchestrator-output-quality` |
| `cases/orchestrator/route-context-bundle.md` | `orchestrator-output-quality` |
| `cases/orchestrator/malformed-config.md` | `orchestrator-output-quality` |
| `cases/orchestrator/missing-references.md` | `orchestrator-output-quality` |
| `cases/orchestrator/invalid-route.md` | `orchestrator-output-quality` |
| `cases/orchestrator/phase-04-timeout-handling.md` | `orchestrator-output-quality` |
| `cases/orchestrator/phase-04-execute-real-cli.md` | `orchestrator-output-quality` |

Every case declares its rubric in a `Use \`evals/rubrics/....md\`` line; `scripts/07-validate-harness.sh` enforces that each reference resolves.
