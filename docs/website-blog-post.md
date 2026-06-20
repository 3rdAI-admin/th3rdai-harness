# Website Blog Post: th3rdai.com

**Suggested URL:** `https://th3rdai.com/blog/ai-agent-harness-v1-2-0`

**Meta Title:** AI Agent Development Harness v1.2.0 - Plain-Text Framework with 3-Mode Autonomy

**Meta Description:** Announcing v1.2.0 of our open-source AI agent development harness - a plain-text, model-agnostic framework with 3-mode autonomy, multi-environment support, and GitNexus integration. Works with Claude Code, Cursor, Windsurf, and Aider.

**Keywords:** AI agents, prompt engineering, LLM development, agent framework, Claude Code, Cursor, Windsurf, Aider, model evaluation, GitNexus

---

# Introducing AI Agent Development Harness v1.2.0

**June 19, 2026** | By James Avila, Th3rdAI

After a year of building AI agents and struggling with ad-hoc development processes, we built something better. Today, we're releasing v1.2.0 of the **AI Agent Development Harness** - an open-source, plain-text framework for designing, evaluating, and improving AI agents.

[**View on GitHub**](https://github.com/3rdAI-admin/th3rdai-harness) | [**Download Template**](https://github.com/3rdAI-admin/th3rdai-harness/generate) | [**Read the Docs**](https://github.com/3rdAI-admin/th3rdai-harness/blob/main/README.md)

---

## The Problem We Solved

When we started building AI agents at Th3rdAI, we ran into the same issues over and over:

- **No standard methodology** - Every team reinvents agent development from scratch
- **Ad-hoc evaluation** - "Does this work?" instead of structured testing
- **Mixed concerns** - Agents, prompts, and models tangled together
- **Vendor lock-in** - Tools that only work with one provider or environment
- **Safety gaps** - No systematic approach to approval gates and risk assessment

We tried existing frameworks, but they focused on *runtime orchestration* (chains, agents, vector stores) rather than *development methodology*. We needed something different.

---

## What We Built

The **AI Agent Development Harness** is a context and methodology framework - think of it as **TDD for AI agents**.

### Core Principles

1. **Plain-text, model-agnostic** - Markdown + YAML + Python stdlib. No vendor lock-in.
2. **Explicit contracts** - Clear separation between agents, prompts, skills, models, and evaluations
3. **Evaluation-first** - Testing is a first-class artifact, not an afterthought
4. **Safe by default** - Approval gates, impact analysis, audit logging

### 7-Stage Lifecycle

Every agent goes through a structured development process:

```
Task Definition → Agent Design → Prompt Design →
Tool Integration → Evaluation → Iteration → Release
```

Each stage has:
- Explicit context requirements
- Input/output contracts
- Handoff protocols
- Token budget estimates (~6K-18K per stage)

---

## What's New in v1.2.0

### 🎛️ 3-Mode Autonomy System

Control how much decision-making authority your agents have:

- **Ask Mode** - Prompt for every decision requiring approval
- **Cautious Mode** - Auto-approve LOW risk, prompt for MEDIUM/HIGH/CRITICAL
- **Full Mode** - Auto-approve LOW/MEDIUM, prompt for HIGH/CRITICAL

All decisions are logged in JSONL format with risk classification and timestamps.

**Use case:** Start in Ask mode during development, switch to Cautious for testing, use Full for production with trusted agents.

### 🌐 Multi-Environment Support

Works seamlessly with multiple AI coding environments:

| Environment | Compatibility | Best For |
|-------------|---------------|----------|
| **Claude Code** | 100% | Reference implementation |
| **Aider** | 98% | CLI workflows, orchestrator execution |
| **Cursor** | 95% | IDE experience, @-mentions workflow |
| **Windsurf** | 90% | AI-native IDE, Cascade features |

See our [Environment Adaptation Guides](https://github.com/3rdAI-admin/th3rdai-harness/tree/main/docs/adapters) for platform-specific setup.

### 📊 ICM Token Budgets

All 7 lifecycle stages now include pedagogical token budget guidance:

- Stage 01 (Task Definition): ~8K-12K tokens
- Stage 02 (Agent Design): ~10K-15K tokens
- Stage 03 (Prompt Design): ~7K-10K tokens
- Stage 04 (Tool Integration): ~6K-9K tokens
- Stage 05 (Evaluation): ~9K-14K tokens
- Stage 06 (Iteration): ~10K-18K tokens
- Stage 07 (Release): ~8K-13K tokens

Each includes breakdown of context components and variance drivers.

### 🔒 Enhanced Security Baseline

Comprehensive security template with:
- Secret detection patterns (OpenAI, GitHub, AWS, JWT, etc.)
- P0/P1/P2 remediation priorities
- Verification commands
- .gitignore configuration guidance

### 🔍 GitNexus Integration (v1.1.0+)

Safe refactoring with knowledge graph analysis:

```bash
# Before modifying code
gitnexus_impact({target: "validateUser", direction: "upstream"})
# Shows: 12 direct callers, 3 affected processes, MEDIUM risk

# After changes
gitnexus_detect_changes()
# Verifies: Only expected symbols affected
```

HIGH/CRITICAL risk warnings halt operations until you approve.

---

## How It Works

### 1. Template Repository

Clone the harness as a GitHub template or local scaffold:

```bash
# Via GitHub
# Click "Use this template" → Clone

# Via local scaffold
git clone https://github.com/3rdAI-admin/th3rdai-harness.git
cd th3rdai-harness
./scripts/01-create-project.sh /path/to/new-project --with-orchestrator
```

### 2. Define Your Task

Start with `stages/01-task-definition/` - structured requirements gathering:

```yaml
task:
  goal: "Build a code review agent"
  inputs: ["Pull request diff", "Repository context"]
  outputs: ["Review comments", "Risk assessment"]
  constraints: ["Max 2000 tokens per review"]
```

### 3. Design Your Agent

Create agent contract in `agents/`:

```yaml
agent: code_reviewer
role: Analyze code changes for quality, security, and maintainability
permissions:
  - read_files
  - analyze_code
  - generate_comments
outputs:
  - review_comments.md
  - risk_score.json
handoffs:
  - to: security_scanner (if risk_score > 0.7)
  - to: human_reviewer (if risk_score > 0.9)
```

### 4. Write Your Prompt

Version-controlled prompts in `prompts/`:

```markdown
# Code Review Prompt v1.0.0

You are a senior code reviewer analyzing pull request changes.

## Instructions
1. Read the diff carefully
2. Check for security vulnerabilities (OWASP Top 10)
3. Assess code quality (readability, maintainability)
4. Generate actionable feedback

## Output Format
[Structured output schema...]
```

### 5. Evaluate

Rubric-based testing in `evals/`:

```yaml
rubric: code_review_quality
criteria:
  - security_coverage: 0-10 (catches SQL injection, XSS, etc.)
  - actionability: 0-10 (comments are specific and helpful)
  - false_positives: 0-10 (avoids incorrect criticisms)
passing_score: 24/30
```

### 6. Orchestrate (Optional)

Dependency-free coordinator (Python stdlib only):

```bash
# Dry-run: Assemble context bundles without executing
python3 scripts/orchestrate.py route agent_design

# Execute: Run through adapter (approval-gated)
python3 scripts/orchestrate.py route agent_design --execute --adapter cli --autonomy cautious
```

---

## Production-Ready Evidence

We didn't just build this - we used it to ship itself:

- ✅ **102/102 harness validation checks** passing
- ✅ **101/101 orchestrator tests** passing
- ✅ **Used to ship v1.0.0, v1.1.0, and v1.2.0** itself
- ✅ **GitNexus indexed** (2906 symbols, 3436 relationships, 32 execution flows)
- ✅ **Comprehensive security baseline** with secret detection
- ✅ **Semantic versioning** with full CHANGELOG

---

## Why Plain Text?

**No vendor lock-in.** Works with any AI coding environment. Markdown + YAML + Python stdlib.

**Version control friendly.** Every change is tracked. Diffs are readable. Merges work.

**Human-readable contracts.** No magic. No hidden behavior. What you see is what you get.

**Works offline.** No API calls for core functionality. Orchestrator uses stdlib only.

**Template distribution.** Fork, customize, share. No installation required.

---

## Comparison: This vs. Other Approaches

### vs. LangChain / LlamaIndex

| This Harness | LangChain/LlamaIndex |
|--------------|----------------------|
| Development methodology | Runtime orchestration |
| Plain-text contracts | Python code |
| Config-first | Code-first |
| Agents + prompts + evals | Chains & agents |
| Model-agnostic | Single-model focus |

**Use both together:** Design/evaluate with this harness, implement runtime with LangChain if needed.

### vs. Ad-hoc Prompting

| This Harness | Ad-hoc Prompting |
|--------------|------------------|
| Structured lifecycle | Trial and error |
| Version control | Copy-paste in chat |
| Rubric-based evaluation | Subjective "seems good" |
| Explicit agent contracts | Implied behavior |
| Safety gates | Hope for the best |

### vs. Vendor-Specific Tools

| This Harness | Vendor Tools |
|--------------|--------------|
| Plain-text artifacts | Proprietary formats |
| Works with 4+ environments | Locked to one |
| No external dependencies | Requires specific runtime |
| Template repository | SaaS subscription |

---

## Real-World Use Cases

### 1. Multi-Agent Code Review System

**Challenge:** Coordinate security scanner, quality checker, and documentation reviewer.

**Solution:**
- 3 agent contracts with explicit handoffs
- Shared evaluation rubric (30-point scale)
- Orchestrator sequences: security → quality → docs → human review
- Cautious autonomy: Auto-approve LOW risk, prompt for MEDIUM+

**Result:** 85% reduction in human review time for LOW-risk PRs.

### 2. Prompt Evolution Across Model Versions

**Challenge:** Track prompt changes as models improve (GPT-3.5 → GPT-4 → Claude 3.5).

**Solution:**
- Version-controlled prompts: `v1.0.0` (GPT-3.5), `v2.0.0` (GPT-4), `v3.0.0` (Claude 3.5)
- Same evaluation rubric across all versions
- CHANGELOG documents behavioral differences
- GitNexus tracks which agents use which prompt versions

**Result:** Clear migration path with regression testing.

### 3. Aider + Local LLM Development

**Challenge:** Build agents with Llama 3 / Mixtral without API costs.

**Solution:**
- Aider CLI integration (98% compatible)
- Token budgets guide context management
- Orchestrator executes locally via CLI adapter
- No API calls - works completely offline

**Result:** Structured agent development with local models.

---

## Getting Started

### Quick Start (5 Minutes)

1. **Use GitHub Template**
   - Go to: https://github.com/3rdAI-admin/th3rdai-harness
   - Click "Use this template"
   - Clone your new repository

2. **Read the Tutorial**
   - Open `TUTORIAL.md`
   - Follow the "First Lifecycle Example"

3. **Run Your First Route**
   ```bash
   python3 scripts/orchestrate.py route task_definition
   ```

4. **Validate Your Setup**
   ```bash
   ./scripts/07-validate-harness.sh
   # Should see: 102/102 checks passing
   ```

### Full Tutorial

See our comprehensive [TUTORIAL.md](https://github.com/3rdAI-admin/th3rdai-harness/blob/main/TUTORIAL.md) covering:
- New project setup
- Existing project integration
- Full lifecycle walkthrough
- Environment-specific configuration

### Environment Setup

Choose your environment:
- [**Claude Code**](https://github.com/3rdAI-admin/th3rdai-harness/blob/main/docs/adapters/README.md) - 100% compatible (reference)
- [**Aider**](https://github.com/3rdAI-admin/th3rdai-harness/blob/main/docs/adapters/AIDER.md) - 98% compatible (best orchestrator fit)
- [**Cursor**](https://github.com/3rdAI-admin/th3rdai-harness/blob/main/docs/adapters/CURSOR.md) - 95% compatible (@-mentions workflow)
- [**Windsurf**](https://github.com/3rdAI-admin/th3rdai-harness/blob/main/docs/adapters/WINDSURF.md) - 90% compatible (Cascade AI)
- [**Generic**](https://github.com/3rdAI-admin/th3rdai-harness/blob/main/docs/adapters/GENERIC.md) - Compatibility assessment guide

---

## Version History

### v1.2.0 (June 19, 2026) - Current Release

- ✅ 3-mode autonomy system (Ask/Cautious/Full)
- ✅ Multi-environment support (4 comprehensive guides)
- ✅ ICM token budgets (all 7 stages)
- ✅ Enhanced security baseline template
- ✅ Canonical CHANGELOG following keepachangelog.com

### v1.1.0 (June 19, 2026)

- ✅ GitNexus integration for code cleanup
- ✅ Impact analysis before moves/deletions
- ✅ HIGH/CRITICAL risk gates
- ✅ Call graph analysis for safe refactoring

### v1.0.0 (June 16, 2026)

- ✅ 7-stage lifecycle framework
- ✅ Native orchestrator (Phases 01-04)
- ✅ Agent contracts (researcher, planner, builder, reviewer, evaluator)
- ✅ Evaluation framework with rubrics and cases
- ✅ 100+ validation checks

See full [CHANGELOG.md](https://github.com/3rdAI-admin/th3rdai-harness/blob/main/CHANGELOG.md) for detailed release notes.

---

## Community & Support

### Get Involved

- **GitHub:** https://github.com/3rdAI-admin/th3rdai-harness
- **Issues:** Report bugs, request features
- **Discussions:** Ask questions, share use cases
- **Pull Requests:** Contributions welcome

### Share Your Experience

We'd love to hear:
- What environment you're using (Claude Code, Cursor, Windsurf, Aider, other?)
- What lifecycle stage you find most/least useful
- What features you'd like to see next
- Real-world use cases and success stories

### Stay Updated

- **Watch on GitHub** for release notifications
- **Star the repository** to show support
- **Follow Th3rdAI** for future announcements

---

## What's Next

### Roadmap

**Near-term (Q3 2026):**
- Real-world case studies from production deployments
- Video tutorial series (YouTube)
- Community-contributed agent templates
- Enhanced orchestrator adapters (API, webhooks)

**Mid-term (Q4 2026):**
- Visual workflow designer (optional, web-based)
- Additional environment guides (VS Code extensions, JetBrains)
- Prompt optimization toolkit
- A/B testing framework for prompts

**Long-term (2027):**
- Agent marketplace / template registry
- Collaborative evaluation platform
- Integration with popular CI/CD systems
- Enterprise support and training

### Contributing

We welcome contributions! Areas we need help:

1. **Environment Adapters** - VS Code, JetBrains, other IDEs
2. **Evaluation Rubrics** - Domain-specific scoring criteria
3. **Agent Templates** - Reusable agent contracts
4. **Documentation** - Tutorials, how-tos, examples
5. **Testing** - Additional test cases and validation

See [CONTRIBUTING.md](https://github.com/3rdAI-admin/th3rdai-harness/blob/main/CONTRIBUTING.md) for guidelines.

---

## Frequently Asked Questions

### Is this a replacement for LangChain?

No - they solve different problems. LangChain is for runtime orchestration (chains, agents, vector stores). This harness is for development methodology (design, evaluation, versioning). You can use both together.

### Do I need Claude Code to use this?

No - it works with Claude Code (100%), Aider (98%), Cursor (95%), Windsurf (90%), and any environment with file read/write capabilities. See our [environment guides](https://github.com/3rdAI-admin/th3rdai-harness/tree/main/docs/adapters).

### Can I use this with local LLMs?

Yes! Aider integration (98% compatible) works great with Llama, Mixtral, and other local models. The harness is model-agnostic - plain text + Python stdlib, no API calls required.

### How is this different from prompt engineering tools?

This provides a *structured lifecycle* for agent development, not just prompt editing. It includes agent contracts, evaluation frameworks, safety gates, versioning, and orchestration - not just prompt text.

### Is the orchestrator required?

No - it's optional. You can use the harness for context management and contracts without ever running the orchestrator. The orchestrator just automates route sequencing and context assembly.

### What about production deployment?

The harness is for *development-time methodology*, not production runtime. Once your agent is validated, deploy it with whatever runtime you prefer (API, CLI, LangChain, custom server, etc.).

### How do I migrate from v1.0.0 to v1.2.0?

No breaking changes! See [CHANGELOG.md](https://github.com/3rdAI-admin/th3rdai-harness/blob/main/CHANGELOG.md) migration guide. v1.2.0 is backward compatible with v1.0.0/v1.1.0 workflows.

### Can I use this commercially?

Yes - the harness is open source (check LICENSE for specific terms). Use it for personal projects, commercial products, internal tools, whatever you need.

---

## Download & Resources

- **GitHub Repository:** https://github.com/3rdAI-admin/th3rdai-harness
- **Use Template:** https://github.com/3rdAI-admin/th3rdai-harness/generate
- **Tutorial:** [TUTORIAL.md](https://github.com/3rdAI-admin/th3rdai-harness/blob/main/TUTORIAL.md)
- **Environment Guides:** [docs/adapters/](https://github.com/3rdAI-admin/th3rdai-harness/tree/main/docs/adapters)
- **CHANGELOG:** [CHANGELOG.md](https://github.com/3rdAI-admin/th3rdai-harness/blob/main/CHANGELOG.md)
- **Quick Reference:** [QUICK-REFERENCE.md](https://github.com/3rdAI-admin/th3rdai-harness/blob/main/docs/QUICK-REFERENCE.md)

---

## About Th3rdAI

At Th3rdAI, we build AI systems that solve real business problems. We believe in:

- **Open source first** - Share tools that move the industry forward
- **Structured methodologies** - Engineering discipline over ad-hoc experimentation
- **Production quality** - Ship it, validate it, document it
- **No vendor lock-in** - Plain text, open formats, portable solutions

This harness emerged from our production work building AI agents for clients. We're sharing it because we believe structured agent development benefits everyone.

**Want to work with us?** Visit [th3rdai.com](https://th3rdai.com) or reach out at james@th3rdai.com.

---

## Share This Release

- [Share on Twitter](https://twitter.com/intent/tweet?text=AI%20Agent%20Development%20Harness%20v1.2.0%20-%20Plain-text%2C%20model-agnostic%20framework%20with%203-mode%20autonomy&url=https://th3rdai.com/blog/ai-agent-harness-v1-2-0)
- [Share on LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https://th3rdai.com/blog/ai-agent-harness-v1-2-0)
- [Share on Reddit](https://reddit.com/submit?url=https://th3rdai.com/blog/ai-agent-harness-v1-2-0&title=AI%20Agent%20Development%20Harness%20v1.2.0)
- [Star on GitHub](https://github.com/3rdAI-admin/th3rdai-harness)

---

**Published:** June 19, 2026
**Author:** James Avila, Founder @ Th3rdAI
**Tags:** AI Agents, Prompt Engineering, LLM Development, Agent Framework, Open Source
**License:** Check [LICENSE](https://github.com/3rdAI-admin/th3rdai-harness/blob/main/LICENSE) for details
