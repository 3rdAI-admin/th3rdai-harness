# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Parallel independent routes** — `orchestrate.py route-batch ROUTE[:TAG] ...`
  runs several lifecycle routes concurrently, each isolated in its own git
  worktree (building on the orchestrator worktree isolation below), so two tasks
  make code changes at once without colliding and `main` stays clean. New
  `scripts/orchestrator/parallel.py` (stdlib `ThreadPoolExecutor`). Each route
  writes run records to its own `runs/<route:tag>/` subdirectory; one route's
  failure never sinks the batch. Refused in `ask` autonomy mode (per-step prompts
  can't interleave across threads) — use `full --yes` or `cautious`. Lifts the
  "parallel execution out of scope" note in the native-orchestrator plans.
- **Orchestrator-driven worktree isolation** — the Native Orchestrator now creates
  and assigns a temporary worktree for configured agents (default: `builder`) when a
  route is run with `orchestrate.py route --execute`, so the step's subprocess runs in
  an isolated feature branch instead of the shared checkout. Previously isolation was
  convention-only (agents were *told* to run `scripts/worktree.sh`) and the orchestrator
  ran every step in the repo root. Configured via a new `execution.isolation` block in
  `configs/execution.yaml`; `--no-isolation` forces legacy in-place behavior. Absent
  config ⇒ unchanged behavior. Wired through `CliAdapter`'s existing (dormant) `cwd`.
- **Worktree-aware risk model** — an isolated step's contained blast radius (work lands
  on a throwaway branch, never shared `main`) downgrades its autonomy risk one level
  (`risk_modifiers.isolated_write` in `configs/autonomy.yaml`;
  `AutonomyManager.apply_isolation_modifier`). Never downgrades protected-path writes or
  `always_block` operations. The `isolated` flag and worktree path are recorded in the
  `runs/autonomy-decisions.jsonl` audit trail.
- **`scripts/worktree.sh gc`** — reclaims stale harness worktree directories (older than
  N days, default 7; `--dry-run` to preview). Deletes only directories; branch refs and
  their commits always persist. Skips the primary checkout and any non-harness directory.
- **Temporary-worktree isolation for builds** — `scripts/worktree.sh`, a portable
  (bash 3.2, sourceable + CLI) helper that isolates code/multi-file changes in a
  throwaway git worktree on a feature branch so concurrent agents don't collide and
  `main` stays clean. Cleanup removes only the directory; the branch ref and its
  commits persist for review. Degrades to in-place work in non-git projects. Wired
  into `agents/builder.agent.md` (Workspace Isolation), `skills/build/build.md`
  (Step 3.5 + cleanup), `CONTRIBUTING.md`, and `GLOSSARY.md`.
- **`/skill-script-audit` skill** — read-only audit of skills for steps that should
  become scripts, plus a history-grounded new-skill backlog (`skills/skill-script-audit/`)

## [1.2.0] - 2026-06-19

### Added
- **3-Mode Autonomy System** - Flexible control over agent decision-making authority
  - `Ask` mode: Prompt for every decision requiring approval
  - `Cautious` mode: Auto-approve LOW risk, prompt for MEDIUM/HIGH/CRITICAL
  - `Full` mode: Auto-approve LOW/MEDIUM, prompt for HIGH/CRITICAL
- Core autonomy infrastructure (9011cef)
  - `configs/autonomy.yaml` with risk classifications and mode definitions
  - `scripts/orchestrator/autonomy_manager.py` with AutonomyManager class
  - Risk classification for common operations (file ops, git, dependencies, execution)
  - Audit logging for all autonomy decisions (JSONL format)
- CLI integration (86fe6b7)
  - `--autonomy` flag for `scripts/orchestrate.py`
  - Integration with execution adapter and approval gates
  - Mode validation and error handling
- Documentation and validation (86fe6b7)
  - Autonomy system documentation in README.md
  - 101/101 orchestrator tests passing (includes autonomy tests)
  - Comprehensive validation report
- **Multi-Environment Support** - Comprehensive environment adaptation guides (f38d858)
  - Aider guide (98% compatible, best orchestrator fit)
  - Cursor guide (95% compatible, @-mentions support)
  - Windsurf guide (90% compatible, Cascade AI integration)
  - Generic template with compatibility scoring system
  - Central index with comparison matrix in `docs/adapters/`
- **ICM Token Budgets** - Pedagogical enhancements to all 7 stage CONTEXT.md files (6fc28ae)
  - Stage-specific token cost estimates (~6K-18K per stage)
  - Breakdown of context loading components
  - Variance drivers documentation
- **Security Baseline Template** - Enhanced `_config/security-baseline.TEMPLATE.md` (6fc28ae)
  - Secret detection patterns (OpenAI, GitHub, AWS, JWT, etc.)
  - P0/P1/P2 remediation priorities
  - Comprehensive .gitignore configuration guidance
  - Verification commands and security resources
- **Canonical CHANGELOG** - Version history following keepachangelog.com (9c648f2, bab1144)
  - Documents v1.0.0, v1.1.0, v1.2.0 with detailed release notes
  - Migration guides and compatibility notes
  - Integrated into README.md and VERSION3.md

### Changed
- Orchestrator execution adapter now respects autonomy mode settings
- Approval gates enhanced with risk-aware decision logic
- Updated validator to detect ICM-compliant "## Token Budget" sections (9ca5666)
- Updated README.md, DISTRIBUTION.md, TUTORIAL.md with environment portability callouts (4312bb6)
- Updated HANDOFF.md to reflect v1.2.0 completion and all enhancements (7f724e0)

### Fixed
- Validator false negative for token budget detection (was expecting table columns, now recognizes section headers)

## [1.1.0] - 2026-06-19

### Added
- **GitNexus Integration for Code Cleanup** - Safe refactoring with impact analysis (aae2203)
  - `gitnexus_impact()` before moves/deletions to assess blast radius
  - HIGH/CRITICAL risk gates that warn users and halt operations
  - `gitnexus_detect_changes()` after each batch to verify scope
  - Call graph analysis for precise reference tracking
- Enhanced `/code-cleanup` skill with GitNexus safety contract
  - Updated `skills/code-cleanup/SKILL.md` with GitNexus procedures
  - Updated `skills/code-cleanup/code-cleanup.md` with explicit tool calls
  - Eval case for code-cleanup skill validation

### Changed
- Code cleanup workflow now uses knowledge graph instead of grep-based reference checking
- Improved safety for refactoring operations with upstream dependency analysis

## [1.0.0] - 2026-06-16

### Added
- **Initial public release** - Production-ready AI agent development harness
- **ICM Phase 1 Pedagogical Enhancements** (4169036)
  - Distribution modes documentation (GitHub template, local scaffold, attach to existing)
  - `_config/conventions.md` - Naming standards and file conventions
  - `docs/QUICK-REFERENCE.md` - 5-layer navigation model and lifecycle overview
  - `.claude/settings.json` - Pre-approved testing commands
- **Native Orchestrator** (01-04 phases)
  - Phase 01: Config parsing and run-log schema
  - Phase 02: Route sequencer with agent/stage/skill/model binding
  - Phase 03: CLI interface with dry-run mode
  - Phase 04: Execution adapter with approval gates
  - `scripts/orchestrate.py` - Main orchestrator CLI
  - `configs/routing.yaml` - Route definitions for 7-stage lifecycle
  - `configs/execution.yaml` - Execution adapter configuration
  - 101/101 orchestrator tests passing
- **7-Stage Lifecycle Framework**
  - Stage 01: Task Definition
  - Stage 02: Agent Design
  - Stage 03: Prompt Design
  - Stage 04: Tool Integration
  - Stage 05: Evaluation
  - Stage 06: Iteration
  - Stage 07: Release
- **Agent Contracts**
  - Researcher Agent (task definition, requirements gathering)
  - Planner Agent (implementation planning, task breakdown)
  - Builder Agent (artifact creation, implementation)
  - Reviewer Agent (quality assurance, risk assessment)
  - Evaluator Agent (rubric-based testing, scoring)
- **Evaluation Framework**
  - `evals/rubrics/` - Scoring criteria for agents, prompts, orchestrator
  - `evals/cases/` - Representative test cases for validation
  - Eval case/rubric coherence validation in harness validator
  - `evals/README.md` - Registry of rubrics and cases
- **Skills System**
  - `/research` - Requirements gathering and analysis
  - `/plan` - Implementation planning
  - `/build` - Artifact creation
  - `/eval` - Rubric-based evaluation
  - `/validate` - Harness validation
  - `/commit` - Safe git workflow
  - `/debug` - Troubleshooting procedures
  - `/revise` - Iteration and refinement
  - `/run` - Workflow execution
  - `/e2e-test` - End-to-end testing (Mode A: browser, Mode B: harness artifacts)
  - `/new-project` - Project bootstrapping
- **Configuration System**
  - `configs/agents.yaml` - Agent profiles and responsibilities
  - `configs/models.yaml` - Model provider guidance
  - `configs/routing.yaml` - Orchestrator route definitions
  - `configs/tools.yaml` - Tool safety policies and approval gates
- **Validation Infrastructure**
  - `scripts/07-validate-harness.sh` - 100+ validation checks
  - `scripts/08-prepare-template-release.sh` - Pre-release validation
  - Harness structure validation (agents, configs, stages, evals)
  - Eval case/rubric coherence enforcement
  - File reference integrity checking
- **Documentation**
  - `FRAMEWORK.md` - Core concepts and operating model
  - `CONTEXT.md` - Routing and stage navigation
  - `AGENTS.md` - Agent registry and quick reference
  - `TUTORIAL.md` - Getting started guide
  - `DISTRIBUTION.md` - Template distribution guide
  - `VERSION3.md` - Version alignment and milestones

### Changed
- Portable skills pattern with `_config/project-notes.md` deployment overlay (81b7267)
- Skills reference project-specific details conditionally
- Orchestrator-specific instructions moved to deployment overlay

### Fixed
- Security: Comprehensive .gitignore patterns for secrets (a22dadd)
- Security: npm dependency vulnerabilities resolved (fd0053b)
- Orchestrator import-root consistency (from scripts.orchestrator)

---

## Version Tags

- `v1.2.0` - Not yet tagged (work complete as of 9ca5666)
- `v1.1.0` - Tagged at aae2203
- `v1.0.0` - Tagged at 5344f04

## Notes

### Compatibility

- **v1.0.0+**: Requires Python 3.8+, works with Claude Code, Cursor, Windsurf, Aider
- **v1.1.0+**: Requires GitNexus MCP server for code-cleanup skill (optional)
- **v1.2.0+**: Backward compatible with v1.0.0/v1.1.0 workflows

### Migration Guide

- **v1.0.0 → v1.1.0**: No breaking changes, code-cleanup skill enhanced (opt-in GitNexus)
- **v1.1.0 → v1.2.0**: No breaking changes, autonomy system opt-in via `--autonomy` flag
- **Environment Adaptation**: See `docs/adapters/` for platform-specific setup

### Links

- [GitHub Repository](https://github.com/th3rdai/th3rdai-harness)
- [Environment Adaptation Guides](./docs/adapters/)
- [Quick Reference](./docs/QUICK-REFERENCE.md)
- [Tutorial](./TUTORIAL.md)
