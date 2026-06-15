---
description: Security diff review and deployment threat model (portable)
name: security
---

# Security — Diff Review and Threat Model

Loaded by `/security` via `skills/security/SKILL.md`.

Implements the **Reviewer Agent** security posture (`agents/reviewer.agent.md`): read-only,
evidence-based, no speculative findings. Every finding must cite `file:line` or a
documented control from the project's baseline overlay. Distinguish **blocking** issues
from hardening recommendations.

## Harness References

- Agent: `agents/reviewer.agent.md`
- Rubrics: `evals/rubrics/agent-output-quality.md`, `evals/rubrics/tool-safety.md`
- Eval case: `evals/cases/code-review/security-bug-review.md`
- Optional baseline: `_config/security-baseline.md` (copy from `_config/security-baseline.TEMPLATE.md`)
- Tool policy: `configs/tools.yaml`
- Deployment overlay (optional): `_config/project-notes.md`

## Input: $ARGUMENTS

- **diff** (default): a diff, PR URL, commit range, or list of changed files
- **threat-model**: deployment scenario, e.g. `LAN bind`, `reverse proxy`, `internet`

Examples:

```text
/security
/security diff HEAD~1
/security threat-model "expose API on home Wi-Fi for mobile testing"
```

## Threat Model (state first)

Before findings, state which model applies:

| Model | Assumption | Minimum bar |
|-------|------------|-------------|
| **Localhost dev** | Operator trusts machine + browser; bind loopback only | Sensitive actions gated; minimal exposure |
| **LAN exposure** | Untrusted devices on the same network may reach the app | Auth on all routes; CSRF on state-changing APIs; no secrets in URLs/storage |
| **Internet / multi-user** | Untrusted users and networks | Full authN/authZ, rate limits, audit logging, OWASP ASVS L2 |

If `_config/security-baseline.md` exists, use its **P0/P1/P2** remediation list for LAN and
internet models instead of inventing priorities.

If the request implies a stricter model than the app supports, say so explicitly.

---

## Mode: diff (default)

### 1. Scope the change

- List changed files and whether they touch: auth, sessions, uploads, admin/config APIs,
  CSP/security headers, WebSocket, rate limits, file/exec tools, backups.
- Read actual code at cited lines — do not infer behavior from names alone.
- If `_config/project-notes.md` exists, check for project-specific security notes or file map.

### 2. Review checklist (apply what is in scope)

**Authentication & session**

- [ ] Secrets in logs, URLs, query params, or error messages
- [ ] Token/cookie storage and XSS blast radius (`localStorage` vs HttpOnly cookies)
- [ ] Constant-time comparison for secrets
- [ ] Auth re-verification on long-lived connections (WebSocket/SSE) after handshake
- [ ] Session fixation, eviction policy, concurrent-request races

**Input & output**

- [ ] Injection (SQL, command, path traversal, SSTI, header injection)
- [ ] Path canonicalization and allowlists for user-supplied names/paths
- [ ] Request/body size limits on streaming or chunked endpoints
- [ ] Upload validation (MIME only vs magic bytes, size caps, virus scanning if required)
- [ ] Output encoding / CSP for new inline script or HTML

**Authorization**

- [ ] Role/scope checks on every state-changing endpoint
- [ ] Privileged actions (shell, file write, admin) gated and auditable
- [ ] Default-deny for dangerous capabilities

**Availability & abuse**

- [ ] Rate limiting on expensive endpoints (LLM, transcribe, search, export)
- [ ] DoS via resource churn (sessions, jobs, uploads)

**Privacy & audit**

- [ ] PII or credentials in telemetry, run logs, or client storage
- [ ] Sensitive operations logged with redaction

### 3. Classify findings

| Level | Meaning | Examples |
|-------|---------|----------|
| **Critical** | Exploitable in the stated threat model | CSRF on state-changing API when LAN-exposed |
| **High** | Serious impact or easy chain | XSS → session theft; path traversal to RCE |
| **Medium** | Meaningful risk or missing control | No rate limit; weak CSP |
| **Low** | Hardening, defense-in-depth | Missing HSTS when TLS off |
| **Info** | Documented accepted risk | Localhost-only design choice |

### 4. Output format

```markdown
# Security Review: <subject>

**Threat model:** <localhost | LAN | internet>
**Scope:** <files/commits>
**Verdict:** block | approve-with-changes | approve

## Findings

| ID | Sev | Location | Issue | Impact | Fix |
|----|-----|----------|-------|--------|-----|
| F1 | High | `path:line` | … | … | … |

## Blocking issues
- …

## Advisory / hardening
- …

## Positive controls observed
- …

## Handoff
- P0 fixes → `/build`
- Plan gaps → `/revise <plan>`
- Eval regression → `evals/cases/code-review/security-bug-review.md`
```

**Rules**

- Do not invent issues unsupported by the diff or code you read.
- Name the vulnerable line or pattern for each finding.
- Propose the smallest fix that addresses root cause.
- Separate blocking issues from nits (per eval case expectations).

---

## Mode: threat-model

Produce a deployment-specific control list — no code changes.

### Process

1. Parse deployment intent from `$ARGUMENTS` (bind address, proxy, users, TLS).
2. Map to threat model table (localhost / LAN / internet).
3. If `_config/security-baseline.md` exists, list **required** controls from its P0/P1/P2
   sections; otherwise use the generic minimum bar from the table above.
4. List **gaps** between required controls and current code/docs (read cited files).
5. State **go / no-go** for the deployment as described.

```markdown
# Threat Model: <scenario>

**Deployment:** …
**Model:** LAN
**Go / no-go:** no-go until P0 complete

## Required controls
- …

## Gaps
- …

## Operator checklist
- [ ] Strong auth secret configured
- [ ] Bind only if necessary; prefer reverse proxy with TLS
- [ ] Disable privileged features unless required
- …
```

---

## Safety and Tooling Notes

- **Read-only** during review — do not patch code unless explicitly asked to implement fixes.
- Do not run destructive commands, exfiltrate secrets, or scan external networks.
- Do not log real tokens, API keys, or `.env` contents in the review output.
- Redact secrets in examples (`<REDACTED>`).
- After fixes, run verify commands from `_config/project-notes.md` when present.

## Success Criteria

- Every finding has cited evidence (`file:line` or baseline ID).
- Severity and impact are explained in plain language.
- Blocking vs advisory is explicit; verdict is clear.
- Fixes are concrete and minimal — not speculative rewrites.
- No false positives from invented attack paths.

## Example Usage

```text
/security diff origin/main...HEAD
/security review PR #42 auth changes
/security threat-model "bind 0.0.0.0 for tablet testing on home Wi-Fi"
```
