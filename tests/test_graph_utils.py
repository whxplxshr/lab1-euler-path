"""Tests for graph validation utilities."""

import networkx as nx
import pytest

from src.graph_utils import get_euler_start_vertex, has_euler_circuit, has_euler_path


class TestHasEulerPath:
    """Tests for has_euler_path function."""

    def test_triangle_has_euler_path(self):
        """Triangle (all even degrees) → Euler circuit → Euler path exists."""
        g = nx.Graph([(1, 2), (2, 3), (3, 1)])
        assert has_euler_path(g) is True

    def test_two_odd_vertices_has_euler_path(self):
        """Graph with exactly 2 odd-degree vertices → Euler path exists."""
        g = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 2)])
        assert has_euler_path(g) is True

    def test_four_odd_vertices_no_euler_path(self):
        """Graph with 4 odd-degree vertices → no Euler path."""
        g = nx.Graph([(1, 2), (3, 4)])
        assert has_euler_path(g) is False

    def test_empty_graph_no_euler_path(self):
        """Graph with no edges → no Euler path."""
        g = nx.Graph()
        g.add_nodes_from([1, 2, 3])
        assert has_euler_path(g) is False

    def test_single_vertex_no_edges(self):
        """Single vertex without edges → no Euler path."""
        g = nx.Graph()
        g.add_node(1)
        assert has_euler_path(g) is False

    def test_disconnected_graph_no_euler_path(self):
        """Disconnected graph with valid degree parity → no Euler path."""
        g = nx.Graph([(1, 2), (2, 1), (3, 4), (4, 3)])
        assert has_euler_path(g) is False

    def test_single_edge(self):
        """Single edge: 2 odd-degree vertices → Euler path exists."""
        g = nx.Graph([(1, 2)])
        assert has_euler_path(g) is True


class TestHasEulerCircuit:
    """Tests for has_euler_circuit function."""

    def test_triangle_has_euler_circuit(self):
        g = nx.Graph([(1, 2), (2, 3), (3, 1)])
        assert has_euler_circuit(g) is True

    def test_path_graph_no_euler_circuit(self):
        """Graph with 2 odd-degree vertices → path, not circuit."""
        g = nx.Graph([(1, 2), (2, 3)])
        assert has_euler_circuit(g) is False

    def test_square_has_euler_circuit(self):
        g = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 1)])
        assert has_euler_circuit(g) is True


class TestGetEulerStartVertex:
    """Tests for get_euler_start_vertex function."""

    def test_start_vertex_from_odd_degree(self):
        """Should return one of the 2 odd-degree vertices."""
        g = nx.Graph([(1, 2), (2, 3)])
        start = get_euler_start_vertex(g)
        assert start in (1, 3)

    def test_start_vertex_circuit(self):
        """For Euler circuit, should return any vertex with edges."""
        g = nx.Graph([(1, 2), (2, 3), (3, 1)])
        start = get_euler_start_vertex(g)
        assert start in (1, 2, 3)

    def test_raises_on_no_euler_path(self):
        """Should raise ValueError when no Euler path exists."""
        g = nx.Graph([(1, 2), (3, 4)])
        with pytest.raises(ValueError, match="does not have an Euler path"):
            get_euler_start_vertex(g)
