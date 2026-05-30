# Task: Native Orchestrator Phase 05 - Enhanced Observability & Error Handling

## Goal

Plan and implement the next iteration of the Native Orchestrator with improvements for:
1. Better error handling and recovery
2. Progress indicators and user feedback
3. Enhanced observability and logging
4. Cancellation handling

## Context

The Native Orchestrator (Phases 01-04) is complete and validated:
- Phase 01: Config reader + run-log writer (stdlib-only YAML parser)
- Phase 02: Sequencer (route → context bundles)
- Phase 03: CLI + eval hook
- Phase 04: Execution adapter (opt-in --execute with approval gates)

Recent evaluation work created 5 new eval cases for error scenarios:
- `malformed-config.md` - YAML syntax errors
- `missing-references.md` - Missing file detection
- `invalid-route.md` - Route validation
- `phase-04-timeout-handling.md` - Subprocess timeouts
- `phase-04-execute-real-cli.md` - End-to-end with real CLI

These eval cases identify areas where the orchestrator should improve its error handling,
user feedback, and robustness.

## Current Gaps

Based on the eval cases and Phase 04 validation:

### Error Handling
- Config parse errors could be more helpful (line numbers, suggestions)
- Missing reference errors should show the full chain (route → agent → field → path)
- Invalid routes should suggest alternatives ("did you mean?")

### Progress & Feedback
- No progress indicators during multi-step execution
- User doesn't know which step is running or how long it might take
- No way to see partial results if execution is interrupted

### Observability
- Limited logging beyond run records
- No structured logs for debugging orchestrator issues
- Hard to trace what happened when something goes wrong

### Cancellation
- No graceful cancellation (Ctrl+C kills subprocess but doesn't clean up)
- Run records incomplete if cancelled mid-execution
- No resume capability after cancellation

## Desired Improvements

### Phase 05 Focus Areas

1. **Error Recovery System**
   - Implement error codes and structured error messages
   - Add "did you mean?" suggestions for typos (routes, files, agents)
   - Enhance YAML parser errors with line/column context
   - Create recovery strategies (retry, skip, abort)

2. **Progress Indicators**
   - Show current step (N/M) during multi-step execution
   - Display estimated time remaining based on historical runs
   - Real-time stdout streaming (optional --stream flag)
   - Progress bar for long-running steps

3. **Structured Logging**
   - Add orchestrator log output (INFO/WARN/ERROR levels)
   - Separate orchestrator logs from agent outputs
   - Log to file with rotation
   - Include trace IDs for correlation across steps

4. **Cancellation & Resume**
   - Handle SIGINT gracefully (finish current step or abort cleanly)
   - Write partial run records on cancellation
   - Add --resume flag to continue from last completed step
   - Store orchestrator state for resume capability

## Success Criteria

Phase 05 is successful when:

1. All 5 new error-handling eval cases pass with improved error messages
2. Multi-step execution shows clear progress indicators
3. Orchestrator logs help diagnose issues without reading code
4. Users can cancel and resume routes without data loss
5. Validator passes (≥98 checks)
6. Orchestrator tests pass (≥70 tests)
7. No breaking changes to Phases 01-04 APIs

## Out of Scope (Future Work)

- Parallel step execution
- Distributed orchestrator (multi-machine)
- Web UI / dashboard
- Model provider direct integration (stays CLI-only)
- Auto-retry on transient failures

## Implementation Approach

Follow harness lifecycle:

1. **Research** (Stage 01) - Analyze error handling patterns, progress indicator libraries, logging frameworks
2. **Plan** (Stage 01) - Create implementation plan for Phase 05
3. **Design** (Stage 02-03) - Design error recovery system, progress indicators
4. **Build** (Stage 04) - Implement Phase 05 features
5. **Evaluate** (Stage 05) - Test against eval cases, validate improvements
6. **Iterate** (Stage 06) - Refine based on feedback
7. **Release** (Stage 07) - Document, commit, update EFFORT.md

## References

- Current implementation: `scripts/orchestrator/` (Phases 01-04)
- Plans: `plans/native-orchestrator/EFFORT.md`
- Eval cases: `evals/cases/orchestrator/` (8 cases total)
- Validation: `scripts/07-validate-harness.sh`
- Tests: `scripts/orchestrator/tests/`

## Task for Researcher Agent

Please research:

1. **Error Handling Patterns** - How do CLI tools like git, cargo, npm handle errors? What makes error messages helpful?
2. **Progress Indicators** - What libraries/patterns work well for Python CLIs? (tqdm, rich, click progress bars?)
3. **Structured Logging** - Best practices for Python logging (stdlib logging vs. loguru vs. structlog?)
4. **Cancellation Handling** - How do long-running Python CLIs handle SIGINT gracefully? Resume patterns?
5. **Existing Gaps** - Review the 5 new eval cases and identify specific improvements needed

Output research notes to `stages/01-task-definition/outputs/orchestrator-phase-05-research.md`

## Task for Planner Agent

Based on the research, create an implementation-ready plan in `plans/native-orchestrator/05-observability-and-errors.md` that includes:

1. Concrete error message improvements with before/after examples
2. Progress indicator implementation approach (library choice, UX design)
3. Logging architecture (where to log, what to log, log levels)
4. Cancellation/resume mechanism design
5. Phased implementation (what to build first, dependencies)
6. Test strategy (how to validate improvements)
7. Backward compatibility plan (no breaking changes to 01-04)

The plan should be detailed enough for the Builder agent to implement without ambiguity.
