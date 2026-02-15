"""Console input utilities for building graphs interactively."""

import networkx as nx


def read_graph_from_console() -> nx.Graph:
    """Read an undirected graph from console input.

    Interactive flow:
        1. Enter number of vertices.
        2. Enter each vertex label (integer).
        3. Enter number of edges.
        4. Enter each edge as two space-separated vertex labels.

    Returns:
        An undirected networkx Graph.

    Raises:
        ValueError: On invalid input (non-integer, negative count, unknown vertex).
    """
    vertex_count_raw = input("Enter the number of vertices: ")
    vertex_count = _parse_positive_int(vertex_count_raw, "Number of vertices")

    vertices = []
    for i in range(1, vertex_count + 1):
        v_raw = input(f"  Vertex {i}: ")
        v = _parse_int(v_raw, f"Vertex {i}")
        if v in vertices:
            raise ValueError(f"Duplicate vertex: {v}")
        vertices.append(v)

    edge_count_raw = input("Enter the number of edges: ")
    edge_count = _parse_non_negative_int(edge_count_raw, "Number of edges")

    graph = nx.Graph()
    graph.add_nodes_from(vertices)

    for i in range(1, edge_count + 1):
        edge_raw = input(f"  Edge {i} (u v): ")
        parts = edge_raw.strip().split()
        if len(parts) != 2:
            raise ValueError(f"Edge {i}: expected 2 values separated by space, got: {edge_raw!r}")
        u = _parse_int(parts[0], f"Edge {i} first vertex")
        v = _parse_int(parts[1], f"Edge {i} second vertex")

        if u not in vertices:
            raise ValueError(f"Edge {i}: vertex {u} is not in the vertex list")
        if v not in vertices:
            raise ValueError(f"Edge {i}: vertex {v} is not in the vertex list")

        graph.add_edge(u, v)

    return graph


def _parse_int(raw: str, label: str) -> int:
    """Parse a string as an integer, raise ValueError with context on failure."""
    stripped = raw.strip()
    if not stripped:
        raise ValueError(f"{label} must not be empty")
    try:
        return int(stripped)
    except ValueError:
        raise ValueError(f"{label} must be an integer, got: {raw!r}")


def _parse_positive_int(raw: str, label: str) -> int:
    """Parse a string as a positive integer (>0)."""
    value = _parse_int(raw, label)
    if value <= 0:
        raise ValueError(f"{label} must be positive, got: {value}")
    return value


def _parse_non_negative_int(raw: str, label: str) -> int:
    """Parse a string as a non-negative integer (>=0)."""
    value = _parse_int(raw, label)
    if value < 0:
        raise ValueError(f"{label} must be non-negative, got: {value}")
    return value
