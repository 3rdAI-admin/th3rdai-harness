# Security Baseline Overlay (Template)

**Purpose:** Per-project security baseline for AI-assisted development. Copy to `_config/security-baseline.md` when bootstrapping a project that uses the portable `/security` skill. Keeps `skills/security/` free of app-specific paths.

**References:**
- Security skill: `skills/security/security.md`
- Tool safety: `configs/tools.yaml`
- Reviewer agent: `agents/reviewer.agent.md`

---

## Threat Model

**Current deployment:** [e.g., localhost dev / LAN exposure / internet multi-user]

| Model | Assumption | Minimum bar |
|-------|------------|-------------|
| **Localhost dev** | Operator trusts machine + browser; bind loopback only | Sensitive actions gated; minimal exposure |
| **LAN exposure** | Untrusted devices on the same network may reach the app | Auth on all routes; CSRF on state-changing APIs; no secrets in URLs/storage |
| **Internet / multi-user** | Untrusted users and networks | Full authN/authZ, rate limits, audit logging, OWASP ASVS L2 |

**Notes:** [Describe your deployment scenario]

---

## Baseline Documents

| Document | Path | Purpose |
|----------|------|---------|
| Assessment report | `<path to WASA/STRIDE/threat-model doc>` | Findings IDs (C1, M1, …) and remediation priority |
| Trust model | `<path to SECURITY.md or equivalent>` | Auth model, deployment assumptions |

---

## Secret Detection Patterns

When scanning for secrets (manual or automated), check these patterns:

### API Keys and Tokens
- OpenAI: `sk-[A-Za-z0-9]{48}` (starts with `sk-`)
- GitHub PAT: `ghp_[A-Za-z0-9]{36}` (starts with `ghp_`)
- AWS Access Key: `AKIA[A-Z0-9]{16}` (starts with `AKIA`)
- Slack: `xox[baprs]-[A-Za-z0-9-]{10,}` (starts with `xox`)
- Google API: `AIza[A-Za-z0-9_-]{35}` (starts with `AIza`)
- Stripe: `sk_live_[A-Za-z0-9]{24}` or `rk_live_[A-Za-z0-9]{24}`
- Anthropic: `sk-ant-[A-Za-z0-9-_]{95,}` (starts with `sk-ant-`)

### Credentials
- Bearer tokens: `Bearer [A-Za-z0-9._-]+`
- JWT tokens: `eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+`
- Database URLs: `postgres://`, `mysql://`, `mongodb://` (with username:password)

### Files and Certificates
- Private keys: `-----BEGIN [A-Z ]+PRIVATE KEY-----`
- Certificates: `.pem`, `.key`, `.crt`, `.p12`, `.pfx`
- Credential files: `*_credentials.json`, `*_secret.json`, `*_key.json`

---

## File Map (for baseline regression audits)

Use when running a project-specific overlay skill (e.g. `skills/security-<project>/`) or
when `/security threat-model` needs concrete paths.

| ID | Topic | Primary files |
|----|-------|---------------|
| C1 | [e.g., Authentication] | `src/auth/`, `src/middleware/auth.ts` |
| C2 | [e.g., API routes] | `src/routes/`, `src/api/` |
| M1 | [e.g., Database access] | `src/db/`, `src/models/` |
| M2 | [e.g., File uploads] | `src/uploads/`, `src/storage/` |

---

## Remediation Priority

### P0 — Blocking (before non-loopback / LAN exposure)

**Security:**
1. No hardcoded secrets in source code, configs, or scripts
2. No real API keys, tokens, or passwords in version control
3. `.gitignore` excludes sensitive files (`.env*`, `*.key`, `*.pem`)
4. Environment variable NAMES only in configs (values loaded at runtime)

**Example P0 checks:**
- [ ] Scan git history for secrets: `git log -p -S "sk-" | grep -E "(sk-|ghp_|AKIA)"`
- [ ] Verify `.env` in .gitignore: `git check-ignore .env`
- [ ] No credentials in source: `rg "(sk-[A-Za-z0-9]{48}|ghp_)" --type-not log`

### P1 — High Priority (before multi-user or exposed port)

**Security:**
1. Secrets loaded from environment variables or secret manager
2. No secrets in logs, error messages, or telemetry
3. API keys rotated if accidentally exposed
4. Auth on all state-changing endpoints (if LAN/internet exposed)

**Example P1 checks:**
- [ ] All API calls use `process.env.API_KEY` or equivalent
- [ ] Logging sanitizes sensitive fields
- [ ] Protected routes have auth middleware
- [ ] CSRF protection on forms

### P2 — Hardening

**Security:**
1. Use secret scanning tools (truffleHog, git-secrets, gitleaks)
2. Separate dev/staging/prod secrets
3. Time-limited tokens where possible
4. Pre-commit hooks prevent secret commits

**Best Practices:**
1. Code review for security changes
2. Automated security testing in CI
3. Regular dependency updates
4. Principle of least privilege

---

## .gitignore Configuration

Ensure your `.gitignore` includes:

```gitignore
# Environment files
.env
.env.*
!.env.example

# Credentials and secrets
*_credentials.json
*_secret.json
*_key.json
*.pem
*.key
*.crt
*.p12
*.pfx

# Database files (if using SQLite)
*.db
*.sqlite
*.sqlite3
```

---

## Verification Commands

```bash
# Security scan
scripts/07-validate-harness.sh                    # Harness structure
python3 -m pytest scripts/orchestrator/tests/     # Orchestrator tests

# Secret detection (add if using tools)
# git secrets --scan                              # git-secrets
# truffleHog filesystem .                         # TruffleHog
# gitleaks detect --source .                      # Gitleaks

# Project-specific verification
# npm test                                        # Your app tests
# npm run lint                                    # Linting
```

---

## Harness Skills

| Skill | Command | Use |
|-------|---------|-----|
| Portable | `/security` | `skills/security/security.md` — diff + threat-model |
| Project overlay | `/security-<project>` | Optional — baseline `wasa` mode against this file |

---

**Last Updated:** [Date]
**Next Review:** [Date, e.g., quarterly]
