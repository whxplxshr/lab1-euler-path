# Pipeline — Euler Path Console Application

> Work progress tracker: epics, implementation status, test results, and notes.

---

## Epic 1: Algorithm Design & Implementation

**Status:** ✅ Done
**Date:** 2026-02-15

### Implemented

| File | Description |
|------|-------------|
| `src/graph_utils.py` | Euler path/circuit validation, start vertex selection |
| `src/hierholzer.py` | Hierholzer's algorithm (iterative DFS, two-stack approach) |
| `src/fleury.py` | Fleury's algorithm (bridge-aware edge-by-edge traversal) |

### Test Results

| Test file | Tests | Result |
|-----------|-------|--------|
| `tests/test_graph_utils.py` | 10 | ✅ All passed |
| `tests/test_hierholzer.py` | 7 | ✅ All passed |
| `tests/test_fleury.py` | 7 | ✅ All passed |
| **Total** | **24** | **✅ 24/24** |

### Manual Verification

```
Hierholzer triangle: [1, 2, 3, 1]       ✅ circuit
Fleury triangle:     [1, 2, 3, 1]       ✅ circuit
Hierholzer path:     [1, 2, 3, 4, 2]    ✅ path (2 odd vertices)
Fleury path:         [1, 2, 3, 4, 2]    ✅ path (2 odd vertices)
Hierholzer square:   [1, 2, 3, 4, 1]    ✅ circuit
Fleury square:       [1, 2, 3, 4, 1]    ✅ circuit
No Euler path:       ValueError raised   ✅ error handling
```

### Notes

- Both algorithms work on `nx.Graph` copies — input graphs are never mutated.
- `mutpy` package not available via pip (will address in Epic 5).

---

## Epic 2: User Interface (Console)

**Status:** 🔲 Not started

### Scope

- Manual graph input via console (vertices + edges).
- JSON file loading.
- Result output to console and JSON file.
- Input validation and error handling.

### Test Results

_No tests yet._

### Notes

_—_

---

## Epic 3: Unit Testing (TDD)

**Status:** 🔲 Not started

### Scope

- Comprehensive PyTest tests for Hierholzer's algorithm.
- Comprehensive PyTest tests for Fleury's algorithm.
- Positive and negative scenarios.

### Test Results

_No tests yet._

### Notes

_—_

---

## Epic 4: Test Design Techniques

**Status:** 🔲 Not started

### Scope

- Boundary Value Analysis tests.
- Equivalence Partitioning tests.
- Statement Testing.
- Branch Testing.

### Test Results

_No tests yet._

### Notes

_—_

---

## Epic 5: Mutation Testing

**Status:** 🔲 Not started

### Scope

- Run MutPy on implemented algorithms.
- Calculate mutation metrics (LCC, MCC, CoveredCodeMSI).
- Analyze and improve test quality based on results.

### Test Results

_No tests yet._

### Notes

- `mutpy` package had installation issues; alternative packages may be needed.
