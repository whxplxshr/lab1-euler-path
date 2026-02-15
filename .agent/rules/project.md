---
trigger: always_on
---

# Project Rule — Euler Path Console Application (Python)

## 🔴 MANDATORY: Document Reading Protocol

**Before ANY implementation, code writing, or planning for this project, the agent MUST read all three documents:**

1. **`docs/General.md`** — Full project description, requirements, tools, and testing methodology.
2. **`docs/Tasks.md`** — Structured task breakdown (5 Epics with subtasks) used as the implementation roadmap.
3. **`docs/project_context.md`** — Document index, summary of each file's purpose, agent protocol.

> [!CAUTION]
> Skipping any of these documents is a **PROTOCOL VIOLATION**. The agent must confirm all three have been read before proceeding.

---

## Language & Stack

| Item | Value | Mandatory |
|------|-------|-----------|
| Language | **Python** | ✅ Strictly enforced |
| Graph library | `networkx` | ✅ |
| Test framework | `PyTest` | ✅ |
| Mutation testing | `MutPy` | ✅ |
| Data format | JSON | ✅ |
| Interface | Console (CLI) | ✅ |

> [!IMPORTANT]
> **No other programming language is permitted.** All code, scripts, and utilities must be written in Python.

---

## Development Methodology

- Follow **TDD** (Test-Driven Development): write tests **before** implementation.
- Apply test design techniques: BVA, Equivalence Partitioning, Statement Testing, Branch Testing.
- Run mutation testing after unit tests are complete to evaluate test quality.

---

## 🔴 MANDATORY: Immediate Verification After Each Task

**Every implemented task MUST be verified for correctness immediately after completion.** A task is NOT considered done until it has been tested and proven to work.

| Task Type | Verification Method |
|-----------|--------------------|
| Algorithm implementation | Prepare test input data, run the algorithm, verify output matches expected result |
| Data loading (JSON/manual) | Create sample input files, run the loader, confirm the graph is constructed correctly |
| Console UI / output | Run the application end-to-end, demonstrate the flow to the user with exact commands |
| Unit tests | Run `pytest` and confirm all tests pass |
| Mutation testing | Run MutPy, show mutation score and analysis |

> [!WARNING]
> **Never mark a task as complete without running it.** If the task is a UI or flow that requires manual interaction, the agent must provide the user with exact steps and commands to verify it themselves.

---

## Agent Skills to Load

The following skills should be loaded when working on this project:

| Skill | When to use |
|-------|-------------|
| `python-patterns` | Always — Python-specific patterns and best practices |
| `clean-code` | Always — code quality rules (Tier 0) |
| `testing-patterns` | Epics 3, 4, 5 — testing methodologies |

---

## Workflow

1. Read all 3 docs (see above).
2. Identify the current task from `Tasks.md`.
3. Load required skills from `.agent/skills/`.
4. Follow TDD: write tests first, then implement.
5. **Immediately verify** the implemented task (see verification table above).
6. Validate with PyTest after each implementation step.
7. Apply mutation testing when unit tests are complete.
