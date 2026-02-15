"""Tests for I/O handler: JSON loading and saving."""

import json
from pathlib import Path

import networkx as nx
import pytest

from src.io_handler import load_graph_from_json, save_result_to_json


class TestLoadGraphFromJson:
    """Tests for load_graph_from_json."""

    def test_load_valid_triangle(self, tmp_path):
        """Load a valid triangle graph from JSON."""
        data = {"vertices": [1, 2, 3], "edges": [[1, 2], [2, 3], [3, 1]]}
        filepath = tmp_path / "triangle.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        graph = load_graph_from_json(str(filepath))

        assert set(graph.nodes()) == {1, 2, 3}
        assert graph.number_of_edges() == 3
        assert graph.has_edge(1, 2)
        assert graph.has_edge(2, 3)
        assert graph.has_edge(3, 1)

    def test_load_valid_path_graph(self, tmp_path):
        """Load a valid path graph with 2 odd-degree vertices."""
        data = {"vertices": [1, 2, 3, 4], "edges": [[1, 2], [2, 3], [3, 4], [4, 2]]}
        filepath = tmp_path / "path.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        graph = load_graph_from_json(str(filepath))

        assert set(graph.nodes()) == {1, 2, 3, 4}
        assert graph.number_of_edges() == 4

    def test_load_vertices_only_no_edges(self, tmp_path):
        """Load a graph with vertices but no edges."""
        data = {"vertices": [1, 2, 3], "edges": []}
        filepath = tmp_path / "no_edges.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        graph = load_graph_from_json(str(filepath))

        assert set(graph.nodes()) == {1, 2, 3}
        assert graph.number_of_edges() == 0

    def test_file_not_found(self):
        """Raise FileNotFoundError for non-existent file."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            load_graph_from_json("nonexistent_file.json")

    def test_invalid_json_syntax(self, tmp_path):
        """Raise ValueError on malformed JSON."""
        filepath = tmp_path / "bad.json"
        filepath.write_text("{invalid json", encoding="utf-8")

        with pytest.raises(ValueError, match="Invalid JSON syntax"):
            load_graph_from_json(str(filepath))

    def test_missing_vertices_key(self, tmp_path):
        """Raise ValueError when 'vertices' key is missing."""
        data = {"edges": [[1, 2]]}
        filepath = tmp_path / "no_vertices.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        with pytest.raises(ValueError, match="Missing required key: 'vertices'"):
            load_graph_from_json(str(filepath))

    def test_missing_edges_key(self, tmp_path):
        """Raise ValueError when 'edges' key is missing."""
        data = {"vertices": [1, 2]}
        filepath = tmp_path / "no_edges_key.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        with pytest.raises(ValueError, match="Missing required key: 'edges'"):
            load_graph_from_json(str(filepath))

    def test_vertices_not_list(self, tmp_path):
        """Raise ValueError when 'vertices' is not a list."""
        data = {"vertices": "abc", "edges": []}
        filepath = tmp_path / "bad_vertices.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        with pytest.raises(ValueError, match="'vertices' must be a list"):
            load_graph_from_json(str(filepath))

    def test_edges_not_list(self, tmp_path):
        """Raise ValueError when 'edges' is not a list."""
        data = {"vertices": [1, 2], "edges": "not_a_list"}
        filepath = tmp_path / "bad_edges.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        with pytest.raises(ValueError, match="'edges' must be a list"):
            load_graph_from_json(str(filepath))

    def test_vertex_not_integer(self, tmp_path):
        """Raise ValueError when a vertex is not an integer."""
        data = {"vertices": [1, "two", 3], "edges": []}
        filepath = tmp_path / "str_vertex.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        with pytest.raises(ValueError, match="Each vertex must be an integer"):
            load_graph_from_json(str(filepath))

    def test_edge_wrong_length(self, tmp_path):
        """Raise ValueError when an edge has wrong number of elements."""
        data = {"vertices": [1, 2, 3], "edges": [[1, 2, 3]]}
        filepath = tmp_path / "bad_edge_len.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        with pytest.raises(ValueError, match="must be a list of 2 elements"):
            load_graph_from_json(str(filepath))

    def test_edge_references_unknown_vertex(self, tmp_path):
        """Raise ValueError when an edge references a vertex not in the list."""
        data = {"vertices": [1, 2], "edges": [[1, 99]]}
        filepath = tmp_path / "unknown_vertex.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        with pytest.raises(ValueError, match="references vertex not in vertices list"):
            load_graph_from_json(str(filepath))

    def test_json_root_not_object(self, tmp_path):
        """Raise ValueError when JSON root is a list instead of object."""
        filepath = tmp_path / "array.json"
        filepath.write_text("[1, 2, 3]", encoding="utf-8")

        with pytest.raises(ValueError, match="JSON root must be an object"):
            load_graph_from_json(str(filepath))

    def test_edge_vertex_not_integer(self, tmp_path):
        """Raise ValueError when edge vertices are not integers."""
        data = {"vertices": [1, 2], "edges": [["a", "b"]]}
        filepath = tmp_path / "str_edge.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        with pytest.raises(ValueError, match="Edge 0 vertices must be integers"):
            load_graph_from_json(str(filepath))

    def test_edge_one_int_one_string(self, tmp_path):
        """Raise ValueError when only one edge vertex is non-integer.

        Mutation target: kills LCR mutant that changes `or` to `and`
        in the edge vertex type check (both must fail for `and` to trigger).
        """
        data = {"vertices": [1, 2], "edges": [[1, "x"]]}
        filepath = tmp_path / "mixed_edge.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        with pytest.raises(ValueError, match="Edge 0 vertices must be integers"):
            load_graph_from_json(str(filepath))


class TestSaveResultToJson:
    """Tests for save_result_to_json."""

    def test_save_valid_result(self, tmp_path):
        """Save a valid Euler path result and verify file contents."""
        filepath = tmp_path / "result.json"
        euler_path = [1, 2, 3, 1]

        save_result_to_json(str(filepath), euler_path, "hierholzer")

        content = json.loads(filepath.read_text(encoding="utf-8"))
        assert content["algorithm"] == "hierholzer"
        assert content["euler_path"] == [1, 2, 3, 1]
        assert content["path_length"] == 3

    def test_save_creates_parent_dirs(self, tmp_path):
        """Save should create parent directories if needed."""
        filepath = tmp_path / "subdir" / "deep" / "result.json"

        save_result_to_json(str(filepath), [1, 2], "fleury")

        assert filepath.exists()
        content = json.loads(filepath.read_text(encoding="utf-8"))
        assert content["algorithm"] == "fleury"

    def test_save_empty_path_raises(self, tmp_path):
        """Raise ValueError when euler_path is empty."""
        filepath = tmp_path / "empty.json"

        with pytest.raises(ValueError, match="euler_path must not be empty"):
            save_result_to_json(str(filepath), [], "hierholzer")

    def test_save_empty_algorithm_raises(self, tmp_path):
        """Raise ValueError when algorithm name is empty."""
        filepath = tmp_path / "no_algo.json"

        with pytest.raises(ValueError, match="algorithm name must not be empty"):
            save_result_to_json(str(filepath), [1, 2], "")
