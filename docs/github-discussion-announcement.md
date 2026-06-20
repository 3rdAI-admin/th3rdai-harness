# 🚀 v1.2.0 Released - 3-Mode Autonomy System + Multi-Environment Support

I'm excited to announce v1.2.0 of the AI Agent Development Harness - a production-ready, plain-text framework for designing, evaluating, and improving AI agents.

## What's New in v1.2.0

### 3-Mode Autonomy System
Control agent decision-making with flexible autonomy modes:
- **Ask:** Prompt for every decision requiring approval
- **Cautious:** Auto-approve LOW risk, prompt for MEDIUM/HIGH/CRITICAL
- **Full:** Auto-approve LOW/MEDIUM, prompt for HIGH/CRITICAL

All with risk classification, audit logging (JSONL format), and integration with the orchestrator CLI.

### Multi-Environment Support
The harness now works seamlessly with:
- **Aider** (98% compatible, best orchestrator fit)
- **Cursor** (95% compatible, @-mentions support)
- **Windsurf** (90% compatible, Cascade AI integration)
- **Claude Code** (100% reference implementation)

See [Environment Adaptation Guides](./docs/adapters/) for setup instructions.

### ICM Token Budgets
All 7 lifecycle stages now include pedagogical token budget guidance (~6K-18K per stage) to help manage context costs.

### Enhanced Security Baseline
Comprehensive template with secret detection patterns and P0/P1/P2 remediation priorities.

## Why This Harness?

- **Plain-text, model-agnostic:** Markdown + YAML + Python stdlib - no vendor lock-in
- **7-stage lifecycle:** Task Definition → Agent Design → Prompt Design → Tool Integration → Evaluation → Iteration → Release
- **Production-ready:** 102/102 validation checks passing
- **Safe by default:** GitNexus impact analysis, approval gates, audit logging

## Quick Start

```bash
# Use as GitHub template
# Click "Use this template" → Clone → Run tutorial

# Or local scaffold
git clone https://github.com/3rdAI-admin/th3rdai-harness.git
cd th3rdai-harness
./scripts/01-create-project.sh /path/to/new-project --with-orchestrator
```

## Learn More

- 📖 [Tutorial](./TUTORIAL.md) - Getting started guide
- 📋 [CHANGELOG](./CHANGELOG.md) - Full release notes
- 🔧 [Environment Adapters](./docs/adapters/) - Platform-specific setup
- 🎯 [Quick Reference](./docs/QUICK-REFERENCE.md) - 5-layer navigation model
- 🚀 [Sharing Guide](./docs/SHARING-GUIDE.md) - How to promote and distribute

## What Makes This Different?

**vs. LangChain/LlamaIndex:** This is a development-time methodology (like TDD for agents), not a runtime orchestration framework. You can use both together - design/evaluate with this harness, implement runtime with LangChain if needed.

**vs. Ad-hoc Prompting:** Explicit contracts for agents, prompts, skills, models, and evaluations. Version control friendly. Structured evaluation framework.

**vs. Vendor-Specific Tools:** Plain-text artifacts work with any environment. No API lock-in. No external dependencies.

## Validation Evidence

- ✅ 102/102 harness structure checks passing
- ✅ 101/101 orchestrator tests passing
- ✅ Used to ship v1.0.0, v1.1.0, and v1.2.0 itself
- ✅ GitNexus impact analysis (2906 symbols, 3436 relationships, 32 execution flows)
- ✅ Comprehensive security baseline with .gitignore patterns

## Feedback Welcome

I'd love to hear:
- What environments you're using (Claude Code, Cursor, Windsurf, Aider, other?)
- What lifecycle stage you find most/least useful
- What features you'd like to see next
- Any issues or questions you encounter

Thanks for checking it out! 🎉

---

**Full release notes:** [CHANGELOG.md](./CHANGELOG.md)
**Tutorial:** [TUTORIAL.md](./TUTORIAL.md)
**Share this release:** [docs/SHARING-GUIDE.md](./docs/SHARING-GUIDE.md)
