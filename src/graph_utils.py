"""Graph validation utilities for Euler path/circuit detection."""

import networkx as nx


def has_euler_path(graph: nx.Graph) -> bool:
    """Check if an undirected graph has an Euler path.

    An Euler path exists if:
    - The graph is connected (considering only vertices with degree > 0).
    - There are exactly 0 or 2 vertices with odd degree.
    """
    if graph.number_of_edges() == 0:
        return False

    # Check connectivity among vertices that have edges
    vertices_with_edges = [v for v in graph.nodes() if graph.degree(v) > 0]
    if not vertices_with_edges:
        return False

    subgraph = graph.subgraph(vertices_with_edges)
    if not nx.is_connected(subgraph):
        return False

    odd_degree_count = sum(1 for v in graph.nodes() if graph.degree(v) % 2 != 0)
    return odd_degree_count in (0, 2)


def has_euler_circuit(graph: nx.Graph) -> bool:
    """Check if an undirected graph has an Euler circuit.

    An Euler circuit exists if:
    - The graph has an Euler path.
    - All vertices have even degree (0 odd-degree vertices).
    """
    if not has_euler_path(graph):
        return False

    odd_degree_count = sum(1 for v in graph.nodes() if graph.degree(v) % 2 != 0)
    return odd_degree_count == 0


def get_euler_start_vertex(graph: nx.Graph) -> int:
    """Return the starting vertex for Euler path traversal.

    - If 2 odd-degree vertices exist, return one of them.
    - If 0 odd-degree vertices exist (circuit), return any vertex with edges.
    - Raises ValueError if no Euler path exists.
    """
    if not has_euler_path(graph):
        raise ValueError("Graph does not have an Euler path")

    odd_degree_vertices = [v for v in graph.nodes() if graph.degree(v) % 2 != 0]

    if odd_degree_vertices:
        return odd_degree_vertices[0]

    # Euler circuit — return any vertex with edges
    for v in graph.nodes():
        if graph.degree(v) > 0:
            return v

    raise ValueError("Graph has no edges")
