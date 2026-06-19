# Rubric: Autonomy Behavior

Score each category from 1 to 5.

| Score | Meaning |
|-------|---------|
| 1 | Broken or non-functional |
| 2 | Partially working with major defects |
| 3 | Functional with notable gaps |
| 4 | Strong with minor issues |
| 5 | Excellent and production-ready |

## Criteria

### Mode Behavior (20 points)

- **Ask Mode Correctness** (5): Always prompts for approval, never auto-approves
- **Cautious Mode Correctness** (5): Auto-approves LOW/MEDIUM, asks for HIGH, blocks CRITICAL
- **Full Mode Correctness** (5): Auto-approves all risk levels
- **Mode Transitions** (5): Switching modes via CLI flag works correctly

### Risk Classification (15 points)

- **Operation Classification** (5): File ops, git ops, code changes classified correctly
- **Protected Write Detection** (5): agents/, configs/, scripts/orchestrator/ trigger HIGH risk
- **Gated Action Detection** (5): tools.yaml phrases trigger HIGH risk

### Audit Logging (20 points)

- **JSONL Format** (5): Valid JSONL with required fields
- **Decision Accuracy** (5): Logged decisions match actual behavior
- **Context Completeness** (5): step, agent, stage, outputs, gated, protected all present
- **Summary Accuracy** (5): Summary counts match audit log entries

### Integration Quality (20 points)

- **CLI Integration** (5): --autonomy flag works, help text clear
- **Driver Integration** (5): execute_route() autonomy_mode parameter works
- **Backward Compatibility** (5): Works without autonomy.yaml (legacy gates)
- **Error Handling** (5): Invalid mode, missing config handled gracefully

### Code Quality (15 points)

- **Test Coverage** (5): Unit tests cover all modes and edge cases
- **Integration Tests** (5): End-to-end tests validate orchestrator integration
- **Code Organization** (5): Clean separation, stdlib-only, graceful fallbacks

### Documentation (10 points)

- **Agent Contract Updates** (3): Builder, Planner, Reviewer contracts updated
- **Skill Updates** (3): code-cleanup, commit, validate skills updated
- **User Documentation** (4): AUTONOMY-MODES.md clear and complete

## Pass Threshold

Autonomy system passes when:

- No criterion scores below 3
- Mode Behavior average ≥ 4.5 (18/20 points)
- Audit Logging average ≥ 4.0 (16/20 points)
- Total score ≥ 80/100 points
- All unit tests pass (24/24)
- All integration tests pass (7/7)
- Manual testing confirms all 3 modes work correctly

## Scoring Guidelines

### Mode Behavior

**5 - Excellent:**
- All 3 modes behave exactly as specified
- Mode transitions instant and reliable
- Edge cases handled (concurrent runs, mode override)

**4 - Strong:**
- All 3 modes work correctly
- Minor issues (cosmetic message formatting, etc.)

**3 - Functional:**
- Modes mostly work but have edge cases
- Some confusion about risk classifications

**2 - Partially working:**
- One or more modes don't work as expected
- Auto-approval logic inconsistent

**1 - Broken:**
- Modes don't differentiate behavior
- Critical failures

### Audit Logging

**5 - Excellent:**
- Perfect JSONL format
- All fields present and accurate
- Summary counts always match
- Append mode works correctly

**4 - Strong:**
- Valid JSONL
- Occasional missing context fields
- Summary mostly accurate

**3 - Functional:**
- Logs created but format issues
- Missing context in some entries
- Summary sometimes wrong

**2 - Partially working:**
- Logs incomplete or malformed
- Summary rarely correct

**1 - Broken:**
- No logs created or unreadable

### Integration Quality

**5 - Excellent:**
- Seamless CLI integration
- Perfect backward compatibility
- Error messages clear and actionable

**4 - Strong:**
- Integration works well
- Minor CLI issues (help text)
- Backward compat verified

**3 - Functional:**
- Basic integration works
- Some breaking changes for existing users
- Error handling basic

**2 - Partially working:**
- Integration brittle
- Backward compat broken

**1 - Broken:**
- Cannot integrate with existing system
