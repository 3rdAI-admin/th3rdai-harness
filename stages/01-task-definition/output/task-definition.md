# Task Definition: v1.1.0 GitNexus Code-Cleanup Enhancement

**Created:** June 19, 2026
**Agent:** Planner (following Stage 01: Task Definition contract)

---

## User Request (Restated)

Enhance the `/code-cleanup` skill to leverage GitNexus MCP tools for precise impact analysis before moving or archiving code files. The current v1.0.0 implementation uses generic "reference-gating" (git grep, manual checks), but the VIRA harness deployment demonstrates a superior approach using explicit `gitnexus_impact()` and `gitnexus_detect_changes()` calls that align with the CLAUDE.md GitNexus rules already in place.

---

## Target Artifact Type

**Skill** enhancement (existing skill revision)

**Affected files:**
- `skills/code-cleanup/SKILL.md` — Skill metadata and safety contract
- `skills/code-cleanup/code-cleanup.md` — Procedure/workflow
- `evals/cases/code-cleanup/` — New eval case (optional but recommended)
- `VERSION3.md` — Documentation of v1.1.0 enhancements

---

## Success Criteria

1. **Code-cleanup skill explicitly uses GitNexus MCP tools:**
   - `gitnexus_impact({target: "...", direction: "upstream"})` before any file move
   - HIGH/CRITICAL risk results → stop and warn user (do not proceed with move)
   - `gitnexus_detect_changes()` after each batch to verify scope matches intent

2. **Safety contract updated:**
   - Replace generic "reference-gating" with explicit GitNexus tool calls
   - Maintain "archive, never delete" principle
   - Preserve batch verification and branch requirements

3. **Validation passes:**
   - `scripts/07-validate-harness.sh` — 100/100 checks
   - All existing skills remain unchanged
   - No breaking changes to skill invocation

4. **Documentation complete:**
   - SKILL.md references GitNexus impact analysis skill
   - Procedure includes explicit tool call examples
   - VERSION3.md documents v1.1.0 enhancement

5. **Optional (recommended):**
   - Create eval case under `evals/cases/code-cleanup/gitnexus-integration.md`
   - Test against plan-quality or tool-safety rubric

---

## Scope Boundaries

### In Scope
- Update `skills/code-cleanup/SKILL.md` safety contract
- Update `skills/code-cleanup/code-cleanup.md` procedure with GitNexus steps
- Cross-reference `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md`
- Document in VERSION3.md under "v1.1.0 Enhancements" section
- Run full harness validation
- Optional: Create eval case

### Out of Scope
- Archive folder rename (`archive/` → `_Archived/`) — defer to v2.0.0
- Changes to other skills
- Changes to GitNexus MCP tools themselves
- Implementation of the enhancement (that's Stage 06: Iteration)
- Changes to orchestrator or core harness infrastructure

---

## Constraints

1. **Template portability:** Skill must work for any bootstrapped project with GitNexus installed
2. **Backward compatibility:** Skill invocation (`/code-cleanup`) remains unchanged
3. **No new dependencies:** GitNexus is already available via MCP, no new installs
4. **v1.0.0 quality bar:** Must pass all validation that v1.0.0 passed

---

## Assumptions

1. GitNexus MCP tools are available in projects using the harness (documented in CLAUDE.md)
2. The `gitnexus_impact()` and `gitnexus_detect_changes()` tools work as documented
3. VIRA harness code-cleanup implementation is tested and functional (we observed it in use)
4. Users prefer explicit tool calls over generic guidance in skill procedures

---

## Dependencies

- `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` exists (already in template)
- `CLAUDE.md` GitNexus section documents impact analysis rules (already present)
- No external dependencies

---

## Clarifying Questions

### Q1: Should we completely replace git grep, or use it as a fallback?
**Impact:** Determines procedure complexity
**Options:**
- A) Replace entirely with GitNexus (cleaner, assumes GitNexus always available)
- B) Use GitNexus as primary, git grep as fallback (more robust, more complex)

**Recommendation:** Option A (replace entirely) — CLAUDE.md already requires GitNexus impact analysis before editing symbols. Code-cleanup should follow the same pattern.

### Q2: Should the eval case be required or optional for v1.1.0?
**Impact:** Release timeline and validation thoroughness
**Options:**
- A) Required — Creates representative case testing GitNexus integration
- B) Optional — Ship faster, add eval case later if issues arise

**Recommendation:** Optional for v1.1.0, but create tracking task for v1.2.0 if deferred.

### Q3: What risk level should trigger a hard stop?
**Impact:** User experience during cleanup operations
**Options:**
- A) HIGH or CRITICAL → stop (conservative, safer)
- B) Only CRITICAL → stop, HIGH → warn but allow proceed (more flexible)

**Recommendation:** Option A (HIGH or CRITICAL stop) — Aligns with CLAUDE.md "NEVER ignore HIGH or CRITICAL risk warnings."

### Q4: Should we update the archive folder convention to `_Archived/` in v1.1.0?
**Impact:** Breaking change for early adopters
**Options:**
- A) Yes, change now (better consistency with `_config/`)
- B) No, defer to v2.0.0 (less disruption)

**Already answered in Scope:** Out of scope, defer to v2.0.0.

### Q5: How should we handle non-code files (docs, configs, assets)?
**Impact:** Procedure clarity for mixed-file cleanups
**Options:**
- A) GitNexus impact analysis for code only, git grep for others
- B) Skip impact analysis for non-code (faster but less safe)

**Recommendation:** Option A — Code gets GitNexus impact, non-code gets git grep reference check. Procedure should be explicit about this split.

---

## Open Questions

1. **User preference:** Does the user want eval case in v1.1.0 or defer? (Owner: User)
2. **Edge case:** How to handle mixed directories (code + docs)? Apply both checks? (Owner: Builder Agent during implementation)

---

## Recommended Next Stage

**Stage 06: Iteration** — This is an enhancement to an existing skill, not a new agent/prompt/config.

**Recommended agent sequence:**
1. Planner Agent — Create detailed implementation plan (this document triggers that)
2. Builder Agent — Apply changes to skill files
3. Reviewer Agent — Review changes against safety contract and portability
4. Evaluator Agent (optional) — Score against plan-quality rubric

**Alternative:** Could use `iteration` route via orchestrator:
```bash
python3 scripts/orchestrate.py route iteration --dry-run
```

---

## Checkpoint

**STOP: User confirmation required before proceeding.**

Please confirm:
- ✅ Scope is correct (GitNexus integration only, no archive rename)
- ✅ Success criteria are achievable
- ✅ Clarifying questions are answered or acceptable as recommended
- ✅ Ready to proceed to planning/iteration stage
