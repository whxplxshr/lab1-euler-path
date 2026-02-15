"""
Epic 4: Branch Testing.
Tests designed to exercise every True/False edge of control flow.
Target: 100% Branch Coverage.
"""

import json
import pytest
import networkx as nx
from unittest.mock import patch, mock_open

from src.graph_utils import has_euler_path, has_euler_circuit, get_euler_start_vertex
from src.fleury import _is_bridge, find_euler_path as fleury_find
from src.io_handler import load_graph_from_json, save_result_to_json

# =================================================================================================
# 1. Graph Utils Branches
# =================================================================================================
class TestGraphUtilsBranch:
    
    def test_branch_has_path_no_edges(self):
        """Branch: if graph.number_of_edges() == 0 -> False."""
        g = nx.Graph()
        g.add_node(1)
        assert has_euler_path(g) is False

    def test_branch_has_path_has_edges_connected(self):
        """Branch: Edges > 0 AND Connected -> True (if parity ok)."""
        g = nx.Graph([(1, 2)])
        assert has_euler_path(g) is True

    def test_branch_has_path_disconnected(self):
        """Branch: Connected -> False."""
        g = nx.Graph([(1, 2), (3, 4)])
        assert has_euler_path(g) is False

    def test_branch_odd_count_0(self):
        """Branch: odd_count == 0 -> True."""
        g = nx.cycle_graph(3) # Triangle
        assert has_euler_path(g) is True

    def test_branch_odd_count_2(self):
        """Branch: odd_count == 2 -> True."""
        g = nx.path_graph(2) # 1-2
        assert has_euler_path(g) is True

    def test_branch_odd_count_4(self):
        """Branch: odd_count (else) -> False."""
        g = nx.star_graph(4) # 4 leaves 1 center = 4 odd
        assert has_euler_path(g) is False


# =================================================================================================
# 2. Fleury Branches (_is_bridge specific)
# =================================================================================================
class TestFleuryBranch:
    
    def test_branch_is_bridge_no_edges(self):
        """Branch: vertices_with_edges empty -> False."""
        g = nx.Graph()
        g.add_node(1) 
        # _is_bridge requires u,v. Add edge first?
        # If we simulate _is_bridge call where removing edge checks works...
        # 1-2. remove 1-2. vertices_with_edges empty.
        g.add_edge(1, 2)
        assert _is_bridge(g, 1, 2) is False

    def test_branch_is_bridge_node_isolated(self):
        """Branch: u not in vertices_with_edges -> True (New Logic)."""
        # 1-2, 3-4. Check 1-2.
        g = nx.Graph([(1, 2), (3, 4)])
        # Remove 1-2. 1 and 2 isolated. 3-4 remain.
        # vertices_with_edges = [3, 4].
        # 1 not in [3, 4].
        # Previous logic: False (not loop).
        # New logic: True (disconnects 1 from 2, effectively a bridge for component {1,2}).
        assert _is_bridge(g, 1, 2) is True

    def test_branch_is_bridge_connected_subgraph(self):
        """Branch: subgraph connected -> False."""
        g = nx.cycle_graph(3) # Triangle 1-2-3-1 (nodes 0,1,2)
        # Check 1-2. Remove. 1-0-2 exists. Connected. Not bridge.
        assert _is_bridge(g, 1, 2) is False

    def test_branch_is_bridge_disconnected_subgraph(self):
        """Branch: subgraph disconnected -> True."""
        g = nx.path_graph(4) # 0-1-2-3
        # Check 1-2. Remove. 0-1 and 2-3 disconnected.
        assert _is_bridge(g, 1, 2) is True


# =================================================================================================
# 3. IO Handler Branches
# =================================================================================================
class TestIOHandlerBranch:

    def test_branch_json_keys_missing_vertices(self, tmp_path):
        """Branch: 'vertices' not in data."""
        f = tmp_path / "no_v.json"
        f.write_text('{"edges": []}', encoding="utf-8")
        with pytest.raises(ValueError, match="Missing required key: 'vertices'"):
            load_graph_from_json(str(f))

    def test_branch_json_keys_missing_edges(self, tmp_path):
        """Branch: 'edges' not in data."""
        f = tmp_path / "no_e.json"
        f.write_text('{"vertices": []}', encoding="utf-8")
        with pytest.raises(ValueError, match="Missing required key: 'edges'"):
            load_graph_from_json(str(f))

    def test_branch_vertices_not_list(self, tmp_path):
        """Branch: vertices not list."""
        f = tmp_path / "v_str.json"
        f.write_text('{"vertices": "s", "edges": []}', encoding="utf-8")
        with pytest.raises(ValueError, match="'vertices' must be a list"):
            load_graph_from_json(str(f))
    
    def test_branch_save_parent_mkdir(self, tmp_path):
        """Branch: parent dir logic (implicit in pathlib)."""
        # Ensure deep path creates dirs
        f = tmp_path / "a" / "b" / "out.json"
        save_result_to_json(str(f), [1], "test")
        assert f.exists()
