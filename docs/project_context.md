# Project Context — Euler Path Console Application

## Purpose

This document serves as the **entry point** for any AI agent or developer starting work on this project. Before implementing any task, you **MUST** read all three documents in the `docs/` folder in the order described below.

---

## Required Reading (3 Documents)

### 1. `General.md` — Full Project Description

**What it contains:**
- Complete problem statement: building a Python console application for finding **Euler paths** in undirected graphs.
- Two algorithms to implement: **Hierholzer's algorithm** (DFS-based) and **Fleury's algorithm** (edge-by-edge approach).
- Input/output requirements: manual console input and JSON file loading; output to console and JSON file.
- Development methodology: **TDD** (Test-Driven Development) with **PyTest**.
- Testing techniques required: Boundary Value Analysis, Equivalence Partitioning, Statement Testing, Branch Testing.
- Mutation testing requirements using **MutPy** (or Pitest equivalent).
- Technology stack: Python, `networkx`, `json`, PyTest, MutPy.

**What to take from it:**
- Understand the full scope of functional and non-functional requirements.
- Know which libraries and tools are mandatory.
- Understand the testing methodology and quality metrics (LCC, MCC, CoveredCodeMSI).

---

### 2. `Tasks.md` — Task Breakdown (Epics & Tasks)

**What it contains:**
- A structured breakdown of the entire project into **5 Epics** with specific subtasks.
- Each task is concrete and actionable, defining exactly **what** to implement and **which tool/library** to use.

**Epic overview:**

| Epic | Title | Focus |
|------|-------|-------|
| 1 | Algorithm Design & Implementation | Hierholzer + Fleury algorithms using `networkx` |
| 2 | User Interface | Manual input, JSON loading, result output |
| 3 | Unit Testing (TDD) | PyTest tests for both algorithms |
| 4 | Test Design Techniques | BVA, Branch Testing with PyTest |
| 5 | Mutation Testing | MutPy/Pitest, mutation metrics analysis |

**What to take from it:**
- Use this as the **implementation roadmap** — tasks are ordered by dependency.
- Each task specifies the exact deliverable and tooling.
- When starting a new task, find the corresponding epic and task in this file first.

---

### 3. `project_context.md` — This File

**What it contains:**
- Summary of each document's purpose and what information to extract.
- The mandatory reading protocol for the agent.
- Quick-reference table of all docs.

---

## Agent Protocol

> **CRITICAL RULE:** At the start of every new task or conversation about this project, the agent **MUST**:
>
> 1. Read `docs/General.md` — to understand the full project context.
> 2. Read `docs/Tasks.md` — to identify the current task and its requirements.
> 3. Read `docs/project_context.md` — to confirm the reading protocol and document structure.
>
> Only after reading all three documents should the agent proceed with any implementation.

## Immediate Verification Rule

Every task must be **verified immediately after implementation**. The agent must:

1. **Algorithms** — prepare test data, run the algorithm, confirm correct output.
2. **Data loading** — create sample JSON, load it, verify the graph structure.
3. **Console UI** — run the app end-to-end and provide the user with exact commands to test manually.
4. **Unit tests** — run `pytest` and show all tests passing.
5. **Mutation testing** — run MutPy and present the mutation score.

> [!IMPORTANT]
> A task is **NOT done** until it is proven to work. No exceptions.

## Technology Constraints

| Constraint | Value |
|-----------|-------|
| Language | **Python** (strictly) |
| Graph library | `networkx` |
| Test framework | `PyTest` |
| Mutation testing | `MutPy` |
| Data format | JSON (input/output) |
| Interface | Console (CLI) |

## Relevant Agent Skills

When implementing tasks for this project, the agent should load the following skills as needed:

- **`python-patterns`** — Python-specific design patterns, coding standards, and best practices.
- **`clean-code`** — General code quality rules (always active per GEMINI.md Tier 0).
- **`testing-patterns`** — Testing methodologies and patterns (for Epics 3–5).
