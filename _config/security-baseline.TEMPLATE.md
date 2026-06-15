# Security baseline overlay (template)

Copy to `_config/security-baseline.md` when bootstrapping a project that uses the portable
`/security` skill. Keeps `skills/security/` free of app-specific paths.

## Baseline documents

| Document | Path | Purpose |
|----------|------|---------|
| Assessment report | `<path to WASA/STRIDE/threat-model doc>` | Findings IDs (C1, M1, …) and remediation priority |
| Trust model | `<path to SECURITY.md or equivalent>` | Auth model, deployment assumptions |

## File map (for baseline regression audits)

Use when running a project-specific overlay skill (e.g. `skills/security-<project>/`) or
when `/security threat-model` needs concrete paths.

| ID | Topic | Primary files |
|----|-------|---------------|
| C1 | … | `src/...` |
| M1 | … | `src/...` |

## Remediation priority

### P0 (before non-loopback / LAN exposure)

1. …

### P1 (before multi-user or exposed port)

1. …

### P2 (hardening)

1. …

## Verification commands

```bash
# After security fixes — fill in for your project
<test command>
<lint or SAST command if any>
```

## Harness skills

| Skill | Command | Use |
|-------|---------|-----|
| Portable | `/security` | `skills/security/security.md` — diff + threat-model |
| Project overlay | `/security-<project>` | Optional — baseline `wasa` mode against this file |
