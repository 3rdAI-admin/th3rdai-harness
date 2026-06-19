# Stage 05: Evaluation

## Purpose

Evaluate agents, prompts, skills, model profiles, and workflows using repeatable rubrics and representative cases.

## Token Budget

**Estimated context cost:** ~9K-14K tokens

**Breakdown:**
- Evaluator agent contract (~1K tokens)
- Evaluation skill (~800 tokens)
- This stage context (~500 tokens)
- evals/README.md (~1K tokens)
- Relevant rubric (~1.5K-2K tokens)
- Relevant eval case (~1K-2K tokens)
- Artifact under test (agent/prompt/skill) (~2K-4K tokens)
- configs/models.yaml (~1K tokens)
- Test outputs and results (~1K-2K tokens)

**Variance drivers:** Complexity of artifact being evaluated, number of rubric criteria, length of test outputs, whether comparison testing (multiple versions/models).

## Inputs

| File | Load | Reason |
|------|------|--------|
| `evals/README.md` | Full | Follow evaluation process |
| Relevant rubric | Full | Apply stable scoring criteria |
| Relevant eval case | Full | Use representative task input |
| Relevant agent contract | Full | Evaluate against responsibilities |
| Relevant prompt or skill | Full | Evaluate the actual artifact under test |
| `configs/models.yaml` | Targeted | Record model profile assumptions |

## Process

1. Select the artifact under evaluation.
2. Select the rubric and eval case before running the evaluation.
3. Record model profile, prompt version, agent, skill, and inputs.
4. Run the evaluation without changing the rubric mid-run.
5. Score outputs and document rationale.
6. Identify failures, regressions, and recommended revisions.
7. Save results under `evals/results/` or `runs/`.

## Outputs

| File | Location | Format |
|------|----------|--------|
| Eval result | `evals/results/<run-id>.md` | Markdown |
| Run record | `runs/<run-id>.md` | Markdown or YAML |
| Revision recommendations | `output/evaluation-findings.md` | Markdown |

## Checkpoint

Do not mark an agent, prompt, skill, or model profile as release-ready if blocking evaluation failures remain unresolved.
