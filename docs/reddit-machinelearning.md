# r/MachineLearning Post

**Title:** `[P] AI Agent Development Harness v1.2.0 - Plain-text framework with 3-mode autonomy`

**Post Body:**

I've been working on a structured methodology for AI agent development and just released v1.2.0 with some significant improvements.

**GitHub:** https://github.com/3rdAI-admin/th3rdai-harness

**What is it?**

A plain-text, model-agnostic harness for designing, evaluating, and improving AI agents. Think of it as applying software engineering best practices (TDD, semantic versioning, CI/CD) to agent development.

**Core Approach:**

- Separate agents, prompts, models, skills, and evaluations
- Explicit contracts for each lifecycle stage
- Plain-text artifacts (markdown + YAML)
- Built-in validation framework (102 checks)

**v1.2.0 Features:**

1. **3-Mode Autonomy System**
   - Ask: Manual approval for every decision
   - Cautious: Auto-approve LOW risk only
   - Full: Auto-approve LOW/MEDIUM risk
   - Risk classification for common operations
   - Audit logging in JSONL format

2. **Multi-Environment Support**
   - Works with Claude Code, Cursor, Windsurf, Aider
   - No vendor lock-in (plain text + Python stdlib)
   - Compatibility scoring (90-98%)

3. **ICM Token Budgets**
   - Context cost estimates per lifecycle stage
   - Helps manage token usage in large projects

4. **GitNexus Integration** (v1.1.0+)
   - Impact analysis before code changes
   - HIGH/CRITICAL risk gates
   - Knowledge graph for safe refactoring

**7-Stage Lifecycle:**

Task Definition → Agent Design → Prompt Design → Tool Integration → Evaluation → Iteration → Release

Each stage has explicit context requirements, inputs/outputs, and handoffs.

**Why Plain Text?**

- Version control friendly
- No external dependencies
- Works with any AI environment
- Human-readable contracts
- No vendor lock-in

**Production-Ready:**

Used to ship v1.0.0, v1.1.0, and v1.2.0 itself. All 102 validation checks passing. Comprehensive safety gates.

Would love feedback from the community - especially if you're working on agent evaluation frameworks or structured prompting methodologies.

**Links:**

- GitHub: https://github.com/3rdAI-admin/th3rdai-harness
- Tutorial: [TUTORIAL.md](https://github.com/3rdAI-admin/th3rdai-harness/blob/main/TUTORIAL.md)
- Environment Guides: [docs/adapters/](https://github.com/3rdAI-admin/th3rdai-harness/tree/main/docs/adapters)
- Changelog: [CHANGELOG.md](https://github.com/3rdAI-admin/th3rdai-harness/blob/main/CHANGELOG.md)
