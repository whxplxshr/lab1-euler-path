"""Tests for console input: interactive graph building."""

import networkx as nx
import pytest

from src.console_input import read_graph_from_console


class TestReadGraphFromConsole:
    """Tests for read_graph_from_console using monkeypatch."""

    def test_valid_triangle_input(self, monkeypatch):
        """Build a triangle graph from valid console input."""
        inputs = iter([
            "3",           # 3 vertices
            "1", "2", "3", # vertex labels
            "3",           # 3 edges
            "1 2", "2 3", "3 1",  # edges
        ])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        graph = read_graph_from_console()

        assert set(graph.nodes()) == {1, 2, 3}
        assert graph.number_of_edges() == 3
        assert graph.has_edge(1, 2)
        assert graph.has_edge(2, 3)
        assert graph.has_edge(3, 1)

    def test_valid_single_edge(self, monkeypatch):
        """Build a graph with a single edge."""
        inputs = iter([
            "2",       # 2 vertices
            "10", "20", # vertex labels
            "1",       # 1 edge
            "10 20",   # edge
        ])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        graph = read_graph_from_console()

        assert set(graph.nodes()) == {10, 20}
        assert graph.has_edge(10, 20)

    def test_vertices_with_no_edges(self, monkeypatch):
        """Build a graph with vertices only, no edges."""
        inputs = iter([
            "2",       # 2 vertices
            "1", "2",  # vertex labels
            "0",       # 0 edges
        ])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        graph = read_graph_from_console()

        assert set(graph.nodes()) == {1, 2}
        assert graph.number_of_edges() == 0

    def test_invalid_vertex_count_not_integer(self, monkeypatch):
        """Raise ValueError when vertex count is not an integer."""
        inputs = iter(["abc"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(ValueError, match="must be an integer"):
            read_graph_from_console()

    def test_invalid_vertex_count_zero(self, monkeypatch):
        """Raise ValueError when vertex count is zero."""
        inputs = iter(["0"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(ValueError, match="must be positive"):
            read_graph_from_console()

    def test_invalid_vertex_count_negative(self, monkeypatch):
        """Raise ValueError when vertex count is negative."""
        inputs = iter(["-1"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(ValueError, match="must be positive"):
            read_graph_from_console()

    def test_invalid_vertex_label_not_integer(self, monkeypatch):
        """Raise ValueError when vertex label is not an integer."""
        inputs = iter(["2", "1", "abc"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(ValueError, match="must be an integer"):
            read_graph_from_console()

    def test_duplicate_vertex_label(self, monkeypatch):
        """Raise ValueError on duplicate vertex label."""
        inputs = iter(["2", "1", "1"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(ValueError, match="Duplicate vertex"):
            read_graph_from_console()

    def test_invalid_edge_format(self, monkeypatch):
        """Raise ValueError when edge input has wrong format."""
        inputs = iter(["2", "1", "2", "1", "1-2"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(ValueError, match="expected 2 values"):
            read_graph_from_console()

    def test_edge_references_unknown_vertex(self, monkeypatch):
        """Raise ValueError when edge references a vertex not in the list."""
        inputs = iter(["2", "1", "2", "1", "1 99"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(ValueError, match="not in the vertex list"):
            read_graph_from_console()

    def test_invalid_edge_count_not_integer(self, monkeypatch):
        """Raise ValueError when edge count is not an integer."""
        inputs = iter(["2", "1", "2", "abc"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(ValueError, match="must be an integer"):
            read_graph_from_console()

    def test_negative_edge_count(self, monkeypatch):
        """Raise ValueError when edge count is negative."""
        inputs = iter(["2", "1", "2", "-1"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(ValueError, match="must be non-negative"):
            read_graph_from_console()

    def test_empty_vertex_count(self, monkeypatch):
        """Raise ValueError when vertex count is empty."""
        inputs = iter([""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(ValueError, match="must not be empty"):
            read_graph_from_console()
