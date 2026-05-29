# Plan: Config Loader + Run-Log Writer

## Goal

Provide dependency-free Python modules that read the harness configs and write run records conforming to `telemetry/run-log-schema.md`.

## Request Type

feature (harness tooling)

## Scope

- In scope: a stdlib-only config reader for the flat YAML subset used by `configs/*.yaml`; a run-record writer that emits the existing Markdown-wrapped YAML format.
- Out of scope: sequencing logic, CLI, any model/API calls.

## Harness Context

- Agent(s): Builder (implements), Reviewer (reviews)
- Skill(s): `skills/build/build.md`, `skills/validate/validate.md`
- Config(s): `configs/agents.yaml`, `configs/models.yaml`, `configs/routing.yaml`, `configs/tools.yaml`
- Telemetry: `telemetry/run-log-schema.md`
- Stage(s): `stages/04-tool-integration/`

## Assumptions

- The YAML the reader handles is a small **indentation-based subset — not flat**: nested mappings 2–3 levels deep (e.g. `routing.yaml`, `agents.yaml`), lists of scalars (`- researcher`), **lists of mappings** (run-record `issues:`), scalar values, `#` comments, and `null`. The reader supports exactly this subset and fails loudly on anything outside it (no folded `>`/`|` block scalars).
- Python 3.9+ is available; no packages may be installed.
- All paths are resolved relative to a detected repo root (from `__file__` or a `PROJECT_ROOT` env override); no absolute, machine-specific paths are hardcoded or persisted.

## Package & Import Convention (locked)

This convention governs all three phases of the effort; do not reopen mid-build.

- **Packages:** `scripts/`, `scripts/orchestrator/`, and `scripts/orchestrator/tests/` are all regular packages (each has `__init__.py`). The fully-qualified package name is `scripts.orchestrator`, matching the repo layout.
- **Import root is the repo root** — the default when running from the repo root, and what pytest/IDEs assume. No `PYTHONPATH` gymnastics.
- **Import style:** absolute and repo-anchored everywhere — `from scripts.orchestrator import config`, `from scripts.orchestrator.runlog import RunRecord`. No `from .` relative imports.
- **Entry point:** `scripts/orchestrate.py` (Phase 03) inserts the repo root (`Path(__file__).resolve().parents[1]`) on `sys.path`, then imports `from scripts.orchestrator import ...`.
- **Tests:** from the repo root, `python3 -m unittest discover -t . -s scripts/orchestrator` (the `-t .` sets the repo root as the top-level dir so `scripts.orchestrator` resolves). Test modules import via `from scripts.orchestrator import ...`.
- An `__init__.py` in `scripts/` is invisible to the shell scripts there; it only affects Python's importer.

## Proposed Approach

Two small modules under `scripts/orchestrator/` (pure stdlib):

- `config.py` — `load_yaml(path) -> dict|list` implementing the documented subset, plus typed helpers `load_agents()`, `load_routing()`, `load_models()`, `load_tools()`. Raise a clear error on unsupported syntax rather than silently misparsing.
- `runlog.py` — `RunRecord` dataclass mirroring `run-log-schema.md` fields; `write(record, dir="runs") -> path` renders the Markdown-wrapped YAML used by existing `runs/examples/`.

## Implementation Steps

1. Create `scripts/orchestrator/__init__.py` and `config.py` with the YAML-subset reader. (validation: unit-parse all four `configs/*.yaml` and assert expected keys)
2. Add typed loader helpers and cross-checks (e.g. every agent `model_profile` exists in models). (validation: matches results of `07-validate-harness.sh` cross-ref checks)
3. Create `runlog.py` with `RunRecord` + `write()`. (validation: generated file parses back via `config.load_yaml` of its embedded block)
4. Add `scripts/orchestrator/tests/` (with `__init__.py`) holding stdlib `unittest` cases; no test framework dependency. (validation: `python3 -m unittest discover -t . -s scripts/orchestrator` passes)

## Validation Criteria

- [ ] `python3 -c "from scripts.orchestrator import config; config.load_agents()"` (from repo root) returns expected structure
- [ ] Round-trip: writing then re-reading a run record preserves fields
- [ ] `python3 -m unittest discover -t . -s scripts/orchestrator` passes
- [ ] `scripts/07-validate-harness.sh` still passes (no structural regressions)

## Safety and Tooling Notes

- No dependency installs (per `configs/tools.yaml`). Stdlib only.
- Read-only against configs; the only writes are run records under `runs/`.

## Risks and Edge Cases

- YAML-subset reader could misparse unexpected syntax → fail loudly with line context, never guess.
- The run-record round-trip (step 3) requires the reader to handle nested mappings **and lists of mappings** (`issues:`), not just flat keys → keep `runlog.write` within the supported subset (single-line/quoted scalars for `notes`, no folded `>`/`|`) so written records re-parse cleanly.
- Future config nesting beyond the subset → documented fallback is generated JSON mirrors.

## Files to Create or Modify

- `scripts/__init__.py` - package marker (makes `scripts.orchestrator` importable from repo root)
- `scripts/orchestrator/__init__.py` - package marker
- `scripts/orchestrator/config.py` - YAML-subset reader + loaders
- `scripts/orchestrator/runlog.py` - run-record writer
- `scripts/orchestrator/tests/__init__.py` - test package marker
- `scripts/orchestrator/tests/test_config.py` - parser tests
- `scripts/orchestrator/tests/test_runlog.py` - writer tests

## Open Questions

- None. Folder location and import strategy are locked in *Package & Import Convention* above: package at `scripts/orchestrator/`, entry `scripts/orchestrate.py` (not a top-level `orchestrator/`).

## Recommended Next Agent

Reviewer
