# r/LocalLLaMA Post

**Title:** `AI Agent Development Harness v1.2.0 - Model-agnostic framework with Aider support (98% compatible)`

**Post Body:**

For those running local LLMs and using Aider, this might be useful - just released v1.2.0 of a structured agent development framework.

**GitHub:** https://github.com/3rdAI-admin/th3rdai-harness

**Why this matters for local LLM users:**

1. **Model-agnostic** - Works with any model (Claude, GPT-4, Llama, Mixtral, etc.)
2. **Aider is the best fit** - 98% compatible, CLI-first design
3. **Token budgets included** - Know exactly how much context each stage uses
4. **No external dependencies** - Python stdlib only, no API calls required

**v1.2.0 Highlights:**

✅ 3-mode autonomy system (Ask/Cautious/Full)
✅ Multi-environment support (Aider, Cursor, Windsurf, Claude Code)
✅ ICM token budgets (~6K-18K per lifecycle stage)
✅ GitNexus impact analysis for safe refactoring

**Aider Integration:**

```bash
pip install aider-chat
cat > configs/execution.yaml << 'EOF'
execution:
  default_adapter: cli
  cli:
    command: ["aider", "--yes", "--message"]
    timeout_seconds: 300
EOF
python3 scripts/orchestrate.py route iteration --execute --adapter cli
```

**Use Case:**

If you're building agents with local models and want:
- Structured evaluation framework
- Repeatable agent design process
- Safety gates for destructive actions
- Version control for prompts
- Token usage estimation

This provides that structure without locking you into a specific provider.

**Links:**

- GitHub: https://github.com/3rdAI-admin/th3rdai-harness
- Aider Setup: [docs/adapters/AIDER.md](https://github.com/3rdAI-admin/th3rdai-harness/blob/main/docs/adapters/AIDER.md)
- Tutorial: [TUTORIAL.md](https://github.com/3rdAI-admin/th3rdai-harness/blob/main/TUTORIAL.md)
