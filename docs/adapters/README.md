# Environment Adaptation Guides

The AI Agent Development Harness is **environment-agnostic** and works with any AI coding assistant that can read markdown and follow instructions. This directory contains adaptation guides for popular environments.

## Quick Selection Guide

| Environment | Compatibility | Effort | Orchestrator | Best For | Guide |
|-------------|---------------|--------|--------------|----------|-------|
| **Aider** | ✅ 98% | 30 min | ✅ Full | CLI workflows, automation | [AIDER.md](./AIDER.md) |
| **Cursor** | ✅ 95% | 1-2 hrs | ⚠️ Via aider | IDE experience, multi-file edits | [CURSOR.md](./CURSOR.md) |
| **Windsurf** | ✅ 90% | 1-2 hrs | ⚠️ Via aider | AI-native IDE, Flow mode | [WINDSURF.md](./WINDSURF.md) |
| **Your Tool** | ❓ Varies | 2-6 hrs | ❓ Depends | Any environment | [GENERIC.md](./GENERIC.md) |

## Which Environment Should I Use?

### For Orchestrator Automation (Recommended)

**Best Choice:** [Aider](./AIDER.md)
- CLI-native, perfect orchestrator integration
- Model-agnostic (Claude, GPT-4, local models)
- Zero-friction setup
- Fast, precise edits
- Works from any environment/editor

### For IDE Experience

**Excellent Choices:**
- **[Cursor](./CURSOR.md):** Strong VS Code-based IDE with good AI integration
- **[Windsurf](./WINDSURF.md):** AI-native IDE with Cascade multi-agent system

### For Maximum Control

Use Aider for execution + your favorite editor:
```bash
# Edit in VS Code, Vim, Emacs, whatever you prefer
vim agents/builder.agent.md

# Execute via Aider + Orchestrator
python3 scripts/orchestrate.py route iteration --execute --adapter cli
```

### For API Integration

Follow the [Generic Guide](./GENERIC.md) to create a custom adapter for your LLM API.

## What's Environment-Agnostic?

The harness core is **100% portable:**

✅ **Harness Structure:**
- `agents/` - Agent contracts
- `skills/` - Reusable procedures
- `prompts/` - Versioned templates
- `configs/` - YAML configuration
- `evals/` - Rubrics and test cases
- `stages/` - Lifecycle stages
- `runs/` - Execution records

✅ **Orchestrator Scripts:**
- Pure Python 3 stdlib
- No external dependencies
- Works with any CLI tool
- Model-agnostic

✅ **Methodology:**
- Agent-driven development
- Lifecycle stages
- Evaluation workflow
- Plan → Implement → Validate cycle

## What Needs Adaptation?

⚠️ **Environment-Specific:**

1. **CLAUDE.md** → Rename to YOUR-ENV.md
2. **Tool references** in agent contracts and skills
3. **MCP servers** (GitNexus, Archon) → Use alternatives
4. **.claude/** directory → Remove if not using Claude Code

**Effort:** 1-6 hours depending on environment

## Quick Start

### Option 1: Use Aider (Easiest)

```bash
# Install aider
pip install aider-chat

# Configure orchestrator
cat > configs/execution.yaml << 'EOF'
execution:
  default_adapter: cli
  cli:
    command: ["aider", "--yes", "--message"]
    timeout_seconds: 300
EOF

# Run!
python3 scripts/orchestrate.py route iteration --execute --adapter cli
```

**Done!** Full harness automation in 5 minutes.

### Option 2: Adapt for Your IDE

1. Choose your guide:
   - [Cursor](./CURSOR.md) for Cursor IDE
   - [Windsurf](./WINDSURF.md) for Windsurf/Codeium
   - [Generic](./GENERIC.md) for other environments

2. Follow the quick start (10-30 minutes)

3. Test with a simple task:
   ```
   Ask your AI: "Act as the Planner agent (see agents/planner.agent.md) and create a plan for adding a /health endpoint"
   ```

4. If that works, you're good to go! ✅

## Adaptation Checklist

Use this checklist for any environment:

- [ ] **Rename CLAUDE.md** → YOUR-ENV.md
- [ ] **Update identity section** with your environment name
- [ ] **Remove .claude/ directory** (if not using Claude Code)
- [ ] **Update agent contracts** with environment-specific tool references
- [ ] **Test basic functionality:**
  - [ ] AI can read agent contracts
  - [ ] AI can follow multi-step procedures
  - [ ] AI can create outputs in stage folders
- [ ] **Configure orchestrator** (if possible):
  - [ ] CLI adapter for command-line tools
  - [ ] Custom adapter for API integration
  - [ ] Or use manual workflow
- [ ] **Document your setup** in `_config/YOUR-ENV-notes.md`

## Common Questions

### Q: Can I use the harness without the orchestrator?

**A:** Yes! The orchestrator is optional. Use the harness methodology manually:

1. Read agent contracts
2. Follow stage CONTEXT.md files
3. Progress through lifecycle stages
4. Document in stage output folders

The orchestrator just automates the bookkeeping.

### Q: Does the harness work with local/open-source models?

**A:** Yes! If you're using Aider, it supports:
- Claude (Anthropic)
- GPT-4 (OpenAI)
- Local models via Ollama (DeepSeek, Code Llama, etc.)
- Any OpenAI-compatible API

### Q: What if my environment isn't listed?

**A:** Follow the [Generic Guide](./GENERIC.md). If your environment can:
- Read markdown files ✅
- Write files ✅
- Follow instructions ✅

Then it can use the harness!

### Q: Can I use multiple environments?

**A:** Absolutely! Common pattern:

```bash
# Edit in your favorite IDE
code agents/builder.agent.md

# Execute with Aider
aider --message "Implement feature X"

# Or via orchestrator
python3 scripts/orchestrate.py route iteration --execute
```

### Q: How do I replace GitNexus MCP?

**A:** Options by environment:

- **Cursor:** Use @Codebase search and "Find All References"
- **Windsurf:** Ask Cascade to find references
- **Aider:** Use ripgrep (`rg`), ctags, or ask Aider
- **Generic:** Built-in IDE features (Shift+F12, Go to Definition, etc.)

GitNexus is helpful but not required.

## Guide Overview

### [AIDER.md](./AIDER.md) - CLI-Based AI Coding

**For:** Developers who prefer CLI tools and automation

**Highlights:**
- ✅ Best orchestrator integration (98% compatible)
- ✅ Zero-friction setup (30 minutes)
- ✅ Model-agnostic (Claude, GPT-4, local models)
- ✅ Works with any editor
- ✅ Perfect for automation and scripting

**Quick Start:** 10 minutes to full automation

### [CURSOR.md](./CURSOR.md) - VS Code-Based AI IDE

**For:** Developers who want IDE features + AI

**Highlights:**
- ✅ Excellent harness support (95% compatible)
- ✅ @-mention system for context
- ✅ Composer for multi-file edits
- ✅ Strong code intelligence
- ✅ Good terminal integration

**Quick Start:** 30 minutes for basic setup

### [WINDSURF.md](./WINDSURF.md) - Codeium AI IDE

**For:** Developers who want AI-native IDE experience

**Highlights:**
- ✅ Strong harness support (90% compatible)
- ✅ Cascade AI multi-agent system
- ✅ Flow mode for complex tasks
- ✅ Automatic context awareness
- ✅ Excellent semantic code search

**Quick Start:** 20 minutes for basic setup

### [GENERIC.md](./GENERIC.md) - Any Environment

**For:** Custom setups, niche tools, API integration

**Highlights:**
- ✅ Comprehensive adaptation guide
- ✅ Custom adapter examples
- ✅ Manual workflow documentation
- ✅ Compatibility scoring
- ✅ Troubleshooting for common issues

**Quick Start:** 2-6 hours depending on environment

## Comparison Matrix

### Feature Support

| Feature | Aider | Cursor | Windsurf | Generic |
|---------|-------|--------|----------|---------|
| **Orchestrator** | ✅ Full | ⚠️ Via Aider | ⚠️ Via Aider | ❓ Custom |
| **Code Intelligence** | ⚠️ External | ✅ Built-in | ✅ Built-in | ❓ Varies |
| **Multi-file Edit** | ✅ Yes | ✅ Composer | ✅ Flow | ❓ Varies |
| **Git Integration** | ✅ Native | ✅ Native | ✅ Native | ❓ Varies |
| **Context Persistence** | ✅ Session | ✅ Chat | ✅ Cascade | ❓ Varies |
| **Terminal Access** | ✅ Built-in | ✅ Built-in | ✅ Built-in | ❓ Varies |
| **Model Choice** | ✅ Any | ⚠️ Limited | ⚠️ Codeium | ✅ Any |

### Best Use Cases

| Environment | Best For |
|-------------|----------|
| **Aider** | Automation, CLI workflows, model experimentation, headless/server |
| **Cursor** | IDE users, VS Code fans, multi-file editing, interactive dev |
| **Windsurf** | AI-native experience, semantic search, Flow mode, beginners |
| **Generic** | Custom setups, corporate environments, specific LLM APIs |

## Contributing Adaptations

Have you adapted the harness for another environment? We'd love to include your guide!

### Template Structure

```markdown
# [Environment Name] Adaptation Guide

**Environment:** [Name] ([Description])
**Compatibility:** [Percentage]
**Effort:** [Time estimate]

## Overview
[What is this environment?]

## Quick Start (XX minutes)
[Minimal steps to get started]

## [Environment]-Specific Features
[What makes this environment unique?]

## Orchestrator Configuration
[How to configure the orchestrator, if possible]

## Adaptation Steps
[Detailed adaptation instructions]

## Best Practices
[Tips for using harness in this environment]

## Troubleshooting
[Common issues and solutions]

## Summary
[Compatibility score, recommended use cases]
```

### Submit Your Guide

1. Fork the repo
2. Create `docs/adapters/YOUR-ENV.md`
3. Follow the template above
4. Submit a pull request
5. We'll review and merge!

## Support

**Need help adapting?**

1. Check existing guides for similar environments
2. Review FRAMEWORK.md for core concepts
3. Start with the [Generic Guide](./GENERIC.md)
4. Open an issue with your environment details

## License

These adaptation guides are part of the AI Agent Development Harness and use the same license as the main project.

---

**Remember:** The harness is tool-agnostic by design. If your AI can read markdown and follow instructions, it can use the harness! 🚀
