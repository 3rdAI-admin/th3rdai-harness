# Open Questions: v1.1.0 GitNexus Code-Cleanup Enhancement

**Created:** June 19, 2026
**Stage:** 01-task-definition

---

## Questions Requiring User Decision

### 1. Eval Case Requirement (v1.1.0 Scope)
**Question:** Should we create an eval case for GitNexus code-cleanup integration in v1.1.0, or defer to v1.2.0?

**Options:**
- **A)** Include in v1.1.0 — More thorough validation, slightly longer timeline
- **B)** Defer to v1.2.0 — Ship enhancement faster, add eval coverage later

**Owner:** User

**Impact:** Release timeline (adds 1-2 hours if included)

**Recommendation:** Optional for v1.1.0 (ship faster), but create Archon task to add in v1.2.0 if deferred.

---

## Questions for Implementation (Builder Agent)

### 2. Mixed File Type Handling
**Question:** When a cleanup batch includes both code files (`.py`, `.ts`, `.js`) and non-code files (`.md`, `.yaml`, `.txt`), should we:

**Options:**
- **A)** Run GitNexus impact on code, git grep on non-code (hybrid approach)
- **B)** Run GitNexus impact on everything (may not work well for non-code)
- **C)** Run git grep on everything (simpler but less precise for code)

**Owner:** Builder Agent (implementation phase)

**Impact:** Procedure complexity and safety level

**Recommendation:** Option A (hybrid) — Aligns with tool strengths. Document the split clearly in procedure.

---

### 3. GitNexus Unavailable Fallback
**Question:** If GitNexus MCP tools are not available (MCP server not running, repo not indexed), should code-cleanup:

**Options:**
- **A)** Fail with clear error message (safe, forces proper setup)
- **B)** Fall back to git grep (works but loses precision)
- **C)** Check availability first, warn user, let them decide

**Owner:** Builder Agent (implementation phase)

**Impact:** Robustness vs. safety tradeoff

**Recommendation:** Option C (check + warn + user decision) — Graceful degradation with informed consent.

---

## Resolved Questions

### ✅ 4. Archive Folder Naming
**Question:** Should we rename `archive/` → `_Archived/` in v1.1.0?

**Resolution:** **No, defer to v2.0.0.** Out of scope for this enhancement. Noted in task definition.

---

### ✅ 5. Risk Threshold for Hard Stop
**Question:** What GitNexus risk level should trigger a hard stop (don't proceed with move)?

**Resolution:** **HIGH or CRITICAL → stop.** Aligns with CLAUDE.md rules: "NEVER ignore HIGH or CRITICAL risk warnings."

---

## Next Steps

Once user confirms question #1 (eval case), proceed to:
- **Stage 06: Iteration** — Create implementation plan
- **Agent:** Planner → detailed plan with file changes and validation steps
