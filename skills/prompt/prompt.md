---
description: Create a focused prompt or prompt-version draft
---

# Prompt - Create Focused Task Prompt

Generate a focused, well-structured prompt for a single task or draft a versioned prompt for the harness. For broad changes, use `/plan` first.

## Harness References

- Stage: `stages/03-prompt-design/`
- Registry: `prompts/registry.md`
- Planner prompt: `prompts/planner/v1.md`
- Reviewer prompt: `prompts/reviewer/v1.md`
- Eval: `evals/rubrics/agent-output-quality.md`

## Input: $ARGUMENTS

- Description of the prompt task
- Optional target agent, skill, model profile, output format, or prompt path

## What Makes a Focused Prompt Task

| Use `/prompt` | Use `/plan` instead |
|---------------|---------------------|
| Draft a prompt for one agent behavior | Redesign a full agent workflow |
| Create a one-off XML prompt | Implement multi-step integration |
| Improve required output sections | Add a new framework layer |
| Add safety constraints to one prompt | Compare several models across evals |
| Create a small prompt test case | Build a full eval suite |

## Process

### 1. Analyze Task

- Clarify scope and target agent or skill
- Identify model/profile assumptions if relevant
- Determine required output format
- Identify validation or eval criteria
- Ask clarifying questions when ambiguous

### 2. Generate Prompt

Create an XML-structured prompt for one-off use or a markdown prompt version for `prompts/<name>/vN.md`.

```xml
<objective>
  <task><clear task statement></task>
  <scope><what is in and out of scope></scope>
</objective>

<context>
  <agent><target agent contract if relevant></agent>
  <skill><target skill if relevant></skill>
  <model_profile><model assumptions or TBD></model_profile>
  <files><relevant files to reference></files>
</context>

<requirements>
  <must>
    <item>1. <requirement></item>
    <item>2. <requirement></item>
  </must>
  <should>
    <item>- <nice to have></item>
  </should>
</requirements>

<constraints>
  <item><constraint> BECAUSE <reason></item>
</constraints>

<output>
  <format><file, markdown, code block, explanation, etc.></format>
  <location><where to save if applicable></location>
</output>

<verification>
  <check><how to verify correctness></check>
  <eval><relevant rubric or case if applicable></eval>
</verification>
```

### 3. Save Prompt

Use one of these locations:

- One-off prompt: `prompts/one-off/<task-name>.md`
- Versioned prompt: `prompts/<prompt-name>/vN.md`
- Prompt changelog: `prompts/<prompt-name>/changelog.md`

Update `prompts/registry.md` for reusable prompt versions.

### 4. Output

```text
PROMPT CREATED: <path>

Summary:
- Task: <task>
- Target agent/skill: <agent or skill>
- Constraints: <key constraints>
- Verification: <checks/evals>

Next:
- Review with Reviewer Agent or run relevant eval.
```

## Example Usage

```text
/prompt "Create a reviewer prompt for checking tool safety"
/prompt "Draft a one-off prompt to summarize eval results"
/prompt "Improve planner prompt output format requirements"
```

## Ambiguity Detection

If the task is unclear, ask:

- What agent or skill should use this prompt?
- Is this one-off or versioned?
- What output format is required?
- Which eval or rubric should verify it?

## Success Criteria

- Task is clearly scoped
- Prompt includes concrete requirements and constraints
- Output format is explicit
- Verification method is specific
- Registry/changelog are updated for reusable prompts
