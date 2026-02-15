"""Fleury's algorithm for finding Euler path/circuit in undirected graphs."""

import networkx as nx

from src.graph_utils import get_euler_start_vertex, has_euler_path


def _is_bridge(graph: nx.Graph, u, v) -> bool:
    """Check if edge (u, v) is a bridge in the graph.

    A bridge is an edge whose removal disconnects the graph
    (among vertices that still have edges).
    """
    graph.remove_edge(u, v)

    # Consider only vertices with remaining edges
    vertices_with_edges = [node for node in graph.nodes() if graph.degree(node) > 0]

    if not vertices_with_edges:
        is_bridge = False
    elif u not in vertices_with_edges or v not in vertices_with_edges:
        # One of the vertices became isolated — not a bridge in the traditional sense,
        # but the edge was the only connection for that vertex
        is_bridge = True
    else:
        subgraph = graph.subgraph(vertices_with_edges)
        is_bridge = not nx.is_connected(subgraph)

    graph.add_edge(u, v)
    return is_bridge


def find_euler_path(graph: nx.Graph) -> list:
    """Find an Euler path or circuit using Fleury's algorithm.

    At each step, prefer non-bridge edges over bridge edges.
    A bridge is only taken when it is the sole remaining edge from the current vertex.

    Args:
        graph: An undirected networkx Graph.

    Returns:
        A list of vertices representing the Euler path.

    Raises:
        ValueError: If the graph does not have an Euler path.
    """
    if not has_euler_path(graph):
        raise ValueError("Graph does not have an Euler path")

    working_graph = graph.copy()
    start = get_euler_start_vertex(working_graph)

    path = [start]
    current = start

    while working_graph.number_of_edges() > 0:
        neighbors = list(working_graph.neighbors(current))

        if not neighbors:
            break

        if len(neighbors) == 1:
            next_vertex = neighbors[0]
        else:
            # Prefer non-bridge edges
            next_vertex = None
            for neighbor in neighbors:
                if not _is_bridge(working_graph, current, neighbor):
                    next_vertex = neighbor
                    break

            # If all edges are bridges, take the first one
            if next_vertex is None:
                next_vertex = neighbors[0]

        working_graph.remove_edge(current, next_vertex)

        # Remove isolated vertices to keep graph clean
        if working_graph.degree(current) == 0 and current != next_vertex:
            working_graph.remove_node(current)
        if next_vertex in working_graph.nodes() and working_graph.degree(next_vertex) == 0:
            pass  # Keep vertex until we move away from it

        current = next_vertex
        path.append(current)

    return path
