"""I/O utilities for loading graphs from JSON and saving results."""

import json
from pathlib import Path

import networkx as nx


def load_graph_from_json(filepath: str) -> nx.Graph:
    """Load an undirected graph from a JSON file.

    Expected JSON format:
        {"vertices": [1, 2, 3], "edges": [[1, 2], [2, 3], [3, 1]]}

    Args:
        filepath: Path to the JSON file.

    Returns:
        An undirected networkx Graph.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the JSON structure is invalid.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    raw = path.read_text(encoding="utf-8")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON syntax: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object with 'vertices' and 'edges' keys")

    if "vertices" not in data:
        raise ValueError("Missing required key: 'vertices'")
    if "edges" not in data:
        raise ValueError("Missing required key: 'edges'")

    vertices = data["vertices"]
    edges = data["edges"]

    if not isinstance(vertices, list):
        raise ValueError("'vertices' must be a list")
    if not isinstance(edges, list):
        raise ValueError("'edges' must be a list")

    for v in vertices:
        if not isinstance(v, int):
            raise ValueError(f"Each vertex must be an integer, got: {v!r}")

    graph = nx.Graph()
    graph.add_nodes_from(vertices)

    for i, edge in enumerate(edges):
        if not isinstance(edge, list) or len(edge) != 2:
            raise ValueError(f"Edge {i} must be a list of 2 elements, got: {edge!r}")

        u, v = edge
        if not isinstance(u, int) or not isinstance(v, int):
            raise ValueError(f"Edge {i} vertices must be integers, got: {edge!r}")

        if u not in vertices or v not in vertices:
            raise ValueError(
                f"Edge {i} references vertex not in vertices list: {edge!r}"
            )

        graph.add_edge(u, v)

    return graph


def save_result_to_json(filepath: str, euler_path: list, algorithm: str) -> None:
    """Save the Euler path result to a JSON file.

    Output format:
        {"algorithm": "hierholzer", "euler_path": [1, 2, 3, 1], "path_length": 3}

    Args:
        filepath: Path to the output JSON file.
        euler_path: List of vertices in the found Euler path.
        algorithm: Name of the algorithm used.

    Raises:
        ValueError: If euler_path is empty or algorithm is empty.
    """
    if not euler_path:
        raise ValueError("euler_path must not be empty")
    if not algorithm:
        raise ValueError("algorithm name must not be empty")

    result = {
        "algorithm": algorithm,
        "euler_path": euler_path,
        "path_length": len(euler_path) - 1,
    }

    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
