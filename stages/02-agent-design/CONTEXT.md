# Stage 02: Agent Design

## Purpose

Create or revise an agent contract: its role, permissions, inputs, outputs, success criteria, and handoff rules. Agents answer the question **who is doing the work?**

## Token Budget

**Estimated context cost:** ~10K-15K tokens

**Breakdown:**
- Planner agent contract (~1K tokens)
- Planning skill (~800 tokens)
- This stage context (~500 tokens)
- Task definition from Stage 01 (~2K-4K tokens)
- FRAMEWORK.md agent section (~1.5K tokens)
- agents/README.md (~800 tokens)
- Existing agent contracts for reference (~3K-5K tokens)
- configs/agents.yaml + configs/tools.yaml (~1K tokens)

**Variance drivers:** Number of existing agents reviewed, complexity of permissions model, extent of configs/tools.yaml updates.

## Inputs

| File | Load | Reason |
|------|------|--------|
| `../01-task-definition/output/task-definition.md` | Full | Use the confirmed task, scope, and success criteria |
| `FRAMEWORK.md` | "Agent" section | Follow the agent contract model |
| `agents/README.md` | Full | Match the existing agent contract conventions |
| Existing `agents/*.agent.md` | Targeted | Reuse patterns; avoid overlapping responsibilities |
| `configs/agents.yaml` | Full | Keep machine-readable agent config in sync |
| `configs/tools.yaml` | Targeted | Align permissions with tool safety policy |

## Process

1. Determine whether an existing agent fits or a new agent is required.
2. Define the agent's role and the single question it answers.
3. Specify inputs, outputs, and explicit success criteria.
4. Define IN SCOPE / OUT OF SCOPE boundaries and required approvals.
5. Specify permissions and reference the relevant tool safety policy.
6. Define handoff rules — which agent or stage receives the output.
7. Update `configs/agents.yaml` to match the contract.

## Outputs

| File | Location | Format |
|------|----------|--------|
| Agent contract | `agents/<name>.agent.md` | Markdown contract |
| Config update | `configs/agents.yaml` | YAML |
| Design notes | `output/agent-design-notes.md` | Markdown |

## Checkpoint

**Stop here and ask the user to review** the agent contract and permission boundaries before proceeding to Stage 03 (Prompt Design). Stop for approval before granting permissions that mutate state, install dependencies, delete files, or commit.
