# Euler Path Finder — User Guide

## Launch

```powershell
cd c:\Users\Nikita\Documents\Тестировка\lab1
python -m src.main
```

---

## Main Menu

```
--- Main Menu ---
  1 — Manual input
  2 — Load from JSON file
  0 — Exit
```

- **1** — Enter a graph manually via console
- **2** — Load a graph from a JSON file
- **0** — Exit the application

After processing, the app returns to the main menu.

---

## Option 1: Manual Input

The app asks step-by-step:

```
Enter the number of vertices: 3
  Vertex 1: 1
  Vertex 2: 2
  Vertex 3: 3
Enter the number of edges: 3
  Edge 1 (u v): 1 2
  Edge 2 (u v): 2 3
  Edge 3 (u v): 3 1
```

**Rules:**
- Vertices are integers, entered one per line
- Edges are entered as two integers separated by a space: `u v`
- Both endpoints of each edge must be in the vertex list
- Duplicate vertices are not allowed

---

## Option 2: JSON File

Enter the full path to a `.json` file:

```
Enter JSON file path: C:\Users\Nikita\Documents\Тестировка\lab1\samples\triangle.json
```

**JSON format:**
```json
{
  "vertices": [1, 2, 3],
  "edges": [[1, 2], [2, 3], [3, 1]]
}
```

---

## Algorithm Selection

```
Choose algorithm:
  1 — Hierholzer
  2 — Fleury
```

- **Hierholzer** — faster, uses iterative DFS with two stacks
- **Fleury** — slower but intuitive, avoids bridges at each step

Both produce the same Euler path for the same graph.

---

## Result Output

```
==================================================
  Algorithm: hierholzer
  Euler path: [1, 2, 3, 1]
  Path length (edges): 3
==================================================

Save result to JSON file? (y/n):
```

If you choose `y`, enter the output file path. The result is saved as:
```json
{
  "algorithm": "hierholzer",
  "euler_path": [1, 2, 3, 1],
  "path_length": 3
}
```

---

## Sample Files (`samples/`)

| File | Type | Description |
|------|------|-------------|
| `single_edge.json` | ✅ Path | 2 vertices, 1 edge — minimal graph |
| `simple_path.json` | ✅ Path | 3 vertices in a line (1-2-3) |
| `triangle.json` | ✅ Circuit | 3 vertices, all connected |
| `square_circuit.json` | ✅ Circuit | 4-vertex ring |
| `path_graph.json` | ✅ Path | 4 vertices, 2 odd-degree |
| `chain_custom_labels.json` | ✅ Path | 5 vertices (10,20,30,40,50) in a line |
| `pentagon_with_chords.json` | ✅ Path | 5-vertex pentagon + 2 chords |
| `two_triangles_circuit.json` | ✅ Circuit | Two triangles sharing vertex 3 |
| `star_cycle_circuit.json` | ✅ Circuit | Star center with outer cycle |
| `large_circuit.json` | ✅ Circuit | 7 vertices, ring + cross-edges |
| `disconnected_no_path.json` | ❌ Error | 2 separate edges — no Euler path |
| `complete_k4_no_path.json` | ❌ Error | K₄ — all vertices odd degree |

---

## Error Cases

- **No Euler path** → `ValueError: Graph does not have an Euler path`
- **File not found** → `FileNotFoundError: File not found: ...`
- **Bad JSON** → `ValueError: Invalid JSON syntax: ...`
- **Missing keys** → `ValueError: Missing required key: 'vertices'`
- **Invalid vertex** → `ValueError: Each vertex must be an integer`
