# Model Matrix

Use this matrix to compare candidate models for agent workflows.

| Workflow | Preferred Model | Backup Model | Reason | Eval Status |
|----------|-----------------|--------------|--------|-------------|
| Research | claude-sonnet-4-6 | claude-haiku-4-5 | Source-grounded synthesis with long context at moderate cost | Default — not yet benchmarked |
| Planning | claude-opus-4-7 | claude-sonnet-4-6 | Deepest structured reasoning and scope control | Default — not yet benchmarked |
| Building | claude-sonnet-4-6 | claude-opus-4-7 | Strong, cost-effective code accuracy and tool safety | Default — not yet benchmarked |
| Reviewing | claude-opus-4-7 | claude-sonnet-4-6 | Best defect detection and risk analysis | Default — not yet benchmarked |
| Evaluation | claude-sonnet-4-6 | claude-haiku-4-5 | Consistent rubric application at temp 0 | Default — not yet benchmarked |

## Notes

- These are sensible capability/cost defaults from the Claude 4.x family, mirrored in `configs/models.yaml`. They are **not yet eval-verified on this repo** — run an eval case across profiles (see `evals/results/_TEMPLATE-model-comparison.md`) and update the Eval Status column with the result.
- The harness is model-agnostic: substitute OpenAI / Gemini / Ollama equivalents per environment (see `models/providers.md`). Record provider, model, temperature, and the reason for any change.
