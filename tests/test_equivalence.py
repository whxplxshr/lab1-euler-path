"""
Epic 4: Equivalence Partitioning (EP) Tests.
Tests representative values from valid and invalid equivalence classes.
"""

import json
import pytest
import networkx as nx
from unittest.mock import patch, mock_open

from src.graph_utils import has_euler_path, has_euler_circuit
from src.hierholzer import find_euler_path as hierholzer_find
from src.fleury import find_euler_path as fleury_find
from src.io_handler import load_graph_from_json
from src.console_input import read_graph_from_console

# =================================================================================================
# 1. Graph Classes EP
# Classes:
# - Valid: Euler Circuit (all even)
# - Valid: Euler Path (exactly 2 odd)
# - Invalid: Disconnected components (even if parity is ok)
# - Invalid: Odd vertices > 2 (e.g., 4, 6)
# =================================================================================================
class TestGraphEquivalence:
    """EP checks for graph validation logic."""

    def test_ep_valid_circuit_partition(self):
        """Class: Connected + All even degrees -> Circuit."""
        # Square with diagonal? No, that makes odd degrees.
        # Just a simple Square: 1-2-3-4-1 (all deg 2)
        g = nx.cycle_graph(4)
        g = nx.relabel_nodes(g, lambda x: x+1)
        assert has_euler_path(g) is True
        assert has_euler_circuit(g) is True

    def test_ep_valid_path_partition(self):
        """Class: Connected + 2 odd degrees -> Path (not circuit)."""
        # House graph: square with triangle roof (1-2, 2-3, 3-4, 4-1, 1-3)
        # nodes: 1(deg3), 2(deg2), 3(deg3), 4(deg2). Odd: 1, 3.
        g = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)])
        assert has_euler_path(g) is True
        assert has_euler_circuit(g) is False

    def test_ep_invalid_parity_partition(self):
        """Class: Connected + >2 odd degrees -> Invalid."""
        # Star graph with 4 leaves: center has degree 4 (even), leaves have degree 1 (odd).
        # 4 odd vertices -> Invalid.
        g = nx.star_graph(4) # center 0 connected to 1,2,3,4
        assert has_euler_path(g) is False

    def test_ep_invalid_disconnected_partition(self):
        """Class: Disconnected components (edges exist in both)."""
        # 1-2 and 3-4.
        g = nx.Graph([(1, 2), (3, 4)])
        assert has_euler_path(g) is False


# =================================================================================================
# 2. Algorithm EP (Testing representative graphs from valid classes)
# =================================================================================================
@pytest.mark.parametrize("algo_find", [hierholzer_find, fleury_find])
class TestAlgorithmsEquivalence:

    def test_ep_valid_circuit_execution(self, algo_find):
        """Class: Valid Circuit execution."""
        g = nx.cycle_graph(6) # Hexagon
        path = algo_find(g)
        assert len(path) == 7
        assert path[0] == path[-1]

    def test_ep_valid_path_execution(self, algo_find):
        """Class: Valid Path execution."""
        # Path: 0-1-2-3
        g = nx.path_graph(4)
        path = algo_find(g)
        assert len(path) == 4
        assert path[0] != path[-1]


# =================================================================================================
# 3. IO Handler EP
# Classes:
# - Valid JSON
# - Invalid: Wrong types (str instead of int)
# - Invalid: Missing structure
# - Invalid: Logical error (edge references unknown node)
# =================================================================================================
class TestIOEquivalence:

    def test_ep_valid_file_partition(self, tmp_path):
        """Class: Valid JSON structure."""
        data = {"vertices": [1, 2], "edges": [[1, 2]]}
        f = tmp_path / "valid.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        g = load_graph_from_json(str(f))
        assert g.number_of_edges() == 1

    def test_ep_invalid_type_partition(self, tmp_path):
        """Class: Invalid data types (string vertices in edge definition)."""
        data = {"vertices": [1, 2], "edges": [["1", "2"]]} # Strings!
        f = tmp_path / "invalid_type.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        with pytest.raises(ValueError, match="must be integers"):
            load_graph_from_json(str(f))

    def test_ep_logical_invalid_partition(self, tmp_path):
        """Class: Logically invalid (reference unknown vertex)."""
        data = {"vertices": [1], "edges": [[1, 2]]} # 2 doesn't exist
        f = tmp_path / "logical_error.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        with pytest.raises(ValueError, match="not in vertices list"):
            load_graph_from_json(str(f))


# =================================================================================================
# 4. Console Input EP
# Classes:
# - Valid: Positive integers
# - Valid: Non-negative integers (for edge count)
# - Invalid: Strings
# - Invalid: Negative numbers
# =================================================================================================
class TestConsoleEquivalence:

    @patch("builtins.input")
    def test_ep_valid_input_class(self, mock_input):
        """Class: All inputs valid integers."""
        # Vertices=2, v1=1, v2=2, Edges=1, e1="1 2"
        mock_input.side_effect = ["2", "1", "2", "1", "1 2"]
        g = read_graph_from_console()
        assert g.number_of_nodes() == 2

    @patch("builtins.input")
    def test_ep_invalid_string_class(self, mock_input):
        """Class: Input is non-numeric string."""
        mock_input.side_effect = ["two"]
        with pytest.raises(ValueError, match="must be an integer"):
            read_graph_from_console()

    @patch("builtins.input")
    def test_ep_invalid_negative_class(self, mock_input):
        """Class: Input is negative integer (where positive required)."""
        mock_input.side_effect = ["-5"]
        with pytest.raises(ValueError, match="must be positive"):
            read_graph_from_console()
