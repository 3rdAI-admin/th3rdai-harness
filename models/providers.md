# Model Providers

This harness is model-agnostic. Use this file to document supported providers, setup assumptions, and tradeoffs.

## Provider Matrix

| Provider | Typical Use | Notes |
|----------|-------------|-------|
| Claude | Planning, coding, review, long-context work | Strong instruction following and code reasoning |
| OpenAI | General reasoning, tool workflows, multimodal tasks | Strong ecosystem and API availability |
| Gemini | Large-context analysis and multimodal workflows | Useful for large document/code analysis |
| Ollama | Local experimentation and privacy-sensitive work | Lower cost, variable quality by model |

## Selection Criteria

Choose a model based on:

- Task complexity
- Context length
- Cost constraints
- Latency needs
- Tool-use requirements
- Data sensitivity
- Evaluation results

## Documentation Rule

When a model is selected for an agent or eval, record:

- Provider
- Model name
- Temperature or equivalent randomness setting
- Relevant limits
- Reason for selection
