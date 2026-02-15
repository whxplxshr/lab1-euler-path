"""Tests for Hierholzer's algorithm."""

import networkx as nx
import pytest

from src.hierholzer import find_euler_path


def _is_valid_euler_path(graph: nx.Graph, path: list) -> bool:
    """Verify that the path is a valid Euler path for the graph.

    Checks:
    1. Path uses every edge exactly once.
    2. Consecutive vertices in the path are connected by an edge.
    """
    if len(path) != graph.number_of_edges() + 1:
        return False

    edge_count = {}
    for u, v in graph.edges():
        key = (min(u, v), max(u, v))
        edge_count[key] = edge_count.get(key, 0) + 1

    path_edge_count = {}
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        key = (min(u, v), max(u, v))
        path_edge_count[key] = path_edge_count.get(key, 0) + 1

    return edge_count == path_edge_count


class TestHierholzer:
    """Tests for Hierholzer's algorithm."""

    def test_triangle_circuit(self):
        """Triangle graph → valid Euler circuit."""
        g = nx.Graph([(1, 2), (2, 3), (3, 1)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        assert path[0] == path[-1]  # circuit

    def test_linear_path(self):
        """Path 1-2-3 → valid Euler path from 1 to 3."""
        g = nx.Graph([(1, 2), (2, 3)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)

    def test_complex_graph_with_euler_path(self):
        """Graph with 2 odd-degree vertices → valid Euler path."""
        g = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 2)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)

    def test_square_circuit(self):
        """Square 1-2-3-4-1 → valid Euler circuit."""
        g = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 1)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        assert path[0] == path[-1]

    def test_raises_on_no_euler_path(self):
        """Graph without Euler path → ValueError."""
        g = nx.Graph([(1, 2), (3, 4)])
        with pytest.raises(ValueError, match="does not have an Euler path"):
            find_euler_path(g)

    def test_single_edge(self):
        """Single edge 1-2 → valid Euler path."""
        g = nx.Graph([(1, 2)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        assert len(path) == 2

    def test_does_not_mutate_input_graph(self):
        """Algorithm should not modify the original graph."""
        g = nx.Graph([(1, 2), (2, 3), (3, 1)])
        original_edges = set(g.edges())
        find_euler_path(g)
        assert set(g.edges()) == original_edges
