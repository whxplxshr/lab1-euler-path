"""Hierholzer's algorithm for finding Euler path/circuit in undirected graphs."""

import networkx as nx

from src.graph_utils import get_euler_start_vertex, has_euler_path


def find_euler_path(graph: nx.Graph) -> list:
    """Find an Euler path or circuit using Hierholzer's algorithm.

    Uses iterative DFS with two stacks:
    1. Current path stack — tracks the DFS traversal.
    2. Circuit list — collects the final Euler path in reverse.

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

    stack = [start]
    path = []

    while stack:
        current = stack[-1]
        neighbors = list(working_graph.neighbors(current))

        if neighbors:
            next_vertex = neighbors[0]
            working_graph.remove_edge(current, next_vertex)
            stack.append(next_vertex)
        else:
            path.append(stack.pop())

    path.reverse()
    return path
