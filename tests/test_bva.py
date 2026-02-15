"""
Epic 4: Boundary Value Analysis (BVA) Tests.
Tests behavior at the boundaries of input domains.
"""

import json
import pytest
import networkx as nx
from unittest.mock import patch, mock_open

from src.graph_utils import has_euler_path, has_euler_circuit, get_euler_start_vertex
from src.hierholzer import find_euler_path as hierholzer_find
from src.fleury import find_euler_path as fleury_find
from src.io_handler import load_graph_from_json, save_result_to_json
from src.console_input import read_graph_from_console


# =================================================================================================
# 1. Graph Utils BVA
# Boundaries: 0 nodes, 1 node, 0 edges, 1 edge (min valid), max odd vertices (0, 2, 4)
# =================================================================================================
class TestGraphUtilsBVA:
    """BVA tests for graph validation utilities."""

    def test_bva_zero_nodes(self):
        """Boundary: 0 nodes -> No Euler path."""
        g = nx.Graph()
        assert has_euler_path(g) is False
        assert has_euler_circuit(g) is False
        with pytest.raises(ValueError, match="no Euler path"):
            get_euler_start_vertex(g)

    def test_bva_one_node_zero_edges(self):
        """Boundary: 1 node, 0 edges -> No Euler path."""
        g = nx.Graph()
        g.add_node(1)
        assert has_euler_path(g) is False

    def test_bva_two_nodes_one_edge(self):
        """Boundary: Min valid Euler path (1 edge)."""
        g = nx.Graph([(1, 2)])
        assert has_euler_path(g) is True
        assert has_euler_circuit(g) is False  # 2 odd vertices
        assert get_euler_start_vertex(g) in (1, 2)

    def test_bva_triangle_min_circuit(self):
        """Boundary: Min valid Euler circuit (3 nodes, 3 edges)."""
        g = nx.Graph([(1, 2), (2, 3), (3, 1)])
        assert has_euler_path(g) is True
        assert has_euler_circuit(g) is True
        # For circuit, any vertex with edges is valid
        assert get_euler_start_vertex(g) in (1, 2, 3)

    def test_bva_boundary_odd_vertices_4(self):
        """Boundary: Just above valid range (2). 4 odd vertices -> Invalid."""
        # Bowtie graph: 1-2, 2-3, 3-1, 1-4, 4-5, 5-1 -> 1 is center
        # Let's make 2 disjpoint edges? No, must be connected.
        # K4 has all 4 vertices with degree 3.
        g = nx.complete_graph(4)
        assert len([v for v in g if g.degree(v) % 2 != 0]) == 4
        assert has_euler_path(g) is False


# =================================================================================================
# 2. Algorithms BVA (Hierholzer & Fleury)
# Boundaries: Minimal graphs, large graphs
# =================================================================================================
@pytest.mark.parametrize("algo_find", [hierholzer_find, fleury_find], ids=["hierholzer", "fleury"])
class TestAlgorithmsBVA:
    """BVA tests for both algorithms."""

    def test_bva_min_path_1_edge(self, algo_find):
        """Boundary: 1 edge graph."""
        g = nx.Graph([(1, 2)])
        path = algo_find(g)
        assert len(path) == 2
        assert set(path) == {1, 2}

    def test_bva_min_circuit_triangle(self, algo_find):
        """Boundary: Triangle (min circuit)."""
        g = nx.Graph([(1, 2), (2, 3), (3, 1)])
        path = algo_find(g)
        assert len(path) == 4
        assert path[0] == path[-1]

    def test_bva_disconnected_with_edges(self, algo_find):
        """Boundary: Disconnected but has edges -> Should raise even if parity is fine?
        Actually has_euler_path checks connectivity.
        Case: 1-2, 3-4 -> 4 odd vertices -> Invalid.
        Case: 2 triangles (1-2-3-1 and 4-5-6-4) -> 0 odd vertices, but disconn."""
        g = nx.Graph([(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4)])
        with pytest.raises(ValueError, match="not have an Euler path"):
            algo_find(g)


# =================================================================================================
# 3. IO Handler BVA
# Boundaries: Empty files, empty JSON structures, single element lists
# =================================================================================================
class TestIOHandlerBVA:
    """BVA tests for I/O functions."""

    def test_bva_load_empty_json_object(self, tmp_path):
        """Boundary: valid JSON object but empty (missing keys)."""
        f = tmp_path / "empty_obj.json"
        f.write_text("{}", encoding="utf-8")
        with pytest.raises(ValueError, match="Missing required key"):
            load_graph_from_json(str(f))

    def test_bva_load_empty_lists(self, tmp_path):
        """Boundary: Both lists empty -> 0 nodes, 0 edges."""
        f = tmp_path / "empty_lists.json"
        f.write_text('{"vertices": [], "edges": []}', encoding="utf-8")
        g = load_graph_from_json(str(f))
        assert g.number_of_nodes() == 0
        assert g.number_of_edges() == 0

    def test_bva_load_single_vertex_no_edges(self, tmp_path):
        """Boundary: 1 vertex list, empty edges."""
        f = tmp_path / "1_node.json"
        f.write_text('{"vertices": [10], "edges": []}', encoding="utf-8")
        g = load_graph_from_json(str(f))
        assert list(g.nodes()) == [10]
        assert g.number_of_edges() == 0

    def test_bva_save_single_node_path(self, tmp_path):
        """Boundary: Path with 1 node (0 edges) - technically invalid for 'path' logic mostly,
        but implementation allows it? No, save_result checks 'euler_path' not empty.
        A path of length 1 (start node only) implies 0 edges traversed."""
        f = tmp_path / "out.json"
        # Logic says: len(path)-1 is length. [1] -> len 0.
        save_result_to_json(str(f), [1], "test_algo")
        data = json.loads(f.read_text("utf-8"))
        assert data["path_length"] == 0
        assert data["euler_path"] == [1]

    def test_bva_save_empty_algo_name(self, tmp_path):
        """Boundary: Empty string for algorithm name."""
        f = tmp_path / "out_err.json"
        with pytest.raises(ValueError, match="algorithm name must not be empty"):
            save_result_to_json(str(f), [1, 2], "")


# =================================================================================================
# 4. Console Input BVA
# Boundaries: 0 vertices, 1 vertex, 0 edges, negative numbers
# =================================================================================================
class TestConsoleInputBVA:
    """BVA tests for console input."""

    @patch("builtins.input")
    def test_bva_zero_vertices(self, mock_input):
        """Boundary: Enter 0 for vertices (should fail, need positive)."""
        mock_input.side_effect = ["0"]
        with pytest.raises(ValueError, match="must be positive"):
            read_graph_from_console()

    @patch("builtins.input")
    def test_bva_one_vertex_zero_edges(self, mock_input):
        """Boundary: 1 vertex, 0 edges -> valid graph (though no path)."""
        # Inputs: N=1, V1='5', E=0
        mock_input.side_effect = ["1", "5", "0"]
        g = read_graph_from_console()
        assert len(g.nodes()) == 1
        assert len(g.edges()) == 0

    @patch("builtins.input")
    def test_bva_min_valid_edge_input(self, mock_input):
        """Boundary: 2 vertices, 1 edge."""
        # Inputs: N=2, V1=1, V2=2, E=1, Edge="1 2"
        mock_input.side_effect = ["2", "1", "2", "1", "1 2"]
        g = read_graph_from_console()
        assert len(g.edges()) == 1
