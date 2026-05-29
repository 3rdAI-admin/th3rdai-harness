---
description: Create new agent harness project from template
---

# New Project - Scaffold Agent Harness Project

Create a new project folder with the AI agent/model development harness preconfigured.

## Harness References

- Generator: `scripts/01-create-project.sh`
- Validation: `scripts/07-validate-harness.sh`
- Framework: `FRAMEWORK.md`
- Routing: `CONTEXT.md`
- Deployment overlay template: `_config/project-notes.TEMPLATE.md` → customize as `project-notes.md`

## Input: $ARGUMENTS

- Project path, such as `~/projects/my-agent-harness` or `./my-harness`

## Process

### 1. Run Generator

Use the maintained bootstrap script:

```bash
scripts/01-create-project.sh
```

When prompted, enter the project path.

Do not manually recreate the folder tree unless the script is unavailable.

### 2. Generated Structure

The new project should include:

```text
<project-path>/
├── README.md
├── FRAMEWORK.md
├── CLAUDE.md
├── CONTEXT.md
├── agents/
├── skills/
├── prompts/
├── models/
├── configs/
├── evals/
├── stages/
├── runs/
├── telemetry/
├── scripts/
├── shared/
└── _config/
```

### 3. Validation

The generator runs validation automatically. If needed, re-run:

```bash
PROJECT_ROOT=<project-path> <project-path>/scripts/07-validate-harness.sh
```

Capture the actual `Passed` / `Warnings` / `Failed` summary from script output.

### 4. Recommended Setup

After creation:

1. Review `CLAUDE.md` and `FRAMEWORK.md`.
2. Copy or customize `_config/project-notes.md` from `_config/project-notes.TEMPLATE.md` (deployment-specific commands and optional tooling).
3. Configure model choices in `configs/models.yaml`.
4. Update or add agent contracts in `agents/`.
5. Add prompt versions in `prompts/`.
6. Add eval cases in `evals/`.

### 5. Output

```text
PROJECT CREATED: <project-path>

Validation:
- scripts/07-validate-harness.sh: passed|failed

Next steps:
1. Review CLAUDE.md and FRAMEWORK.md
2. Configure configs/models.yaml
3. Start with /plan or stages/01-task-definition/
```

## Example Usage

```text
/new-project ~/projects/my-agent-harness
/new-project ./model-eval-harness
```

## Error Handling

- Directory exists: ask whether to overwrite files or choose a different path.
- Permission denied: suggest a different path.
- Validation fails: report failed checks and fix the generated structure before proceeding.
- Template not found: verify this harness template path is accessible.

## Success Criteria

- Project directory created
- Harness folders and required files present
- Validation passes
- Next configuration steps are clear
