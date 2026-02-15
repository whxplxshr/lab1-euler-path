"""Comprehensive unit tests for Fleury's algorithm (Epic 3)."""

import networkx as nx
import pytest

from src.fleury import find_euler_path, _is_bridge


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


# ---------------------------------------------------------------------------
# Euler CIRCUIT tests (all vertices have even degree)
# ---------------------------------------------------------------------------
class TestFleuryCircuit:
    """Graphs where all vertices have even degree → Euler circuit."""

    def test_triangle_circuit(self):
        """Triangle 1-2-3 → 3 edges, all deg 2, Euler circuit."""
        g = nx.Graph([(1, 2), (2, 3), (3, 1)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        assert path[0] == path[-1], "Circuit must start and end at same vertex"

    def test_square_circuit(self):
        """Square 1-2-3-4-1 → 4 edges, all deg 2, Euler circuit."""
        g = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 1)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        assert path[0] == path[-1]

    def test_figure_eight_circuit(self):
        """Two triangles sharing vertex 1 (figure-8) → 6 edges, all even degrees."""
        g = nx.Graph([(1, 2), (2, 3), (3, 1), (1, 4), (4, 5), (5, 1)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        assert path[0] == path[-1]

    def test_hexagon_circuit(self):
        """Hexagon 1-2-3-4-5-6-1 → 6 edges, all deg 2, Euler circuit."""
        g = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        assert path[0] == path[-1]

    def test_octagon_circuit(self):
        """Octagon 1-2-3-4-5-6-7-8-1 → 8 edges, all deg 2, Euler circuit."""
        g = nx.Graph()
        for i in range(1, 9):
            g.add_edge(i, i + 1 if i < 8 else 1)
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        assert path[0] == path[-1]


# ---------------------------------------------------------------------------
# Euler PATH tests (exactly 2 odd-degree vertices)
# ---------------------------------------------------------------------------
class TestFleuryPath:
    """Graphs with exactly 2 odd-degree vertices → Euler path (not circuit)."""

    def test_single_edge_path(self):
        """Single edge 1-2 → simplest Euler path."""
        g = nx.Graph([(1, 2)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        assert len(path) == 2

    def test_linear_chain_path(self):
        """Chain 1-2-3 → 2 edges, Euler path from 1 to 3."""
        g = nx.Graph([(1, 2), (2, 3)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        assert path[0] != path[-1], "Path (not circuit) must have different endpoints"

    def test_four_node_with_two_odd_vertices(self):
        """4-node graph with 2 odd-degree vertices → Euler path."""
        g = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 2)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)

    def test_longer_chain_five_nodes(self):
        """Chain 1-2-3-4-5 → 4 edges, Euler path."""
        g = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 5)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        assert len(path) == 5

    def test_triangle_with_tail(self):
        """Triangle 1-2-3 plus tail 3-4 → 4 edges, odd vertices: 1, 4."""
        g = nx.Graph([(1, 2), (2, 3), (3, 1), (3, 4)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        odd_vertices = {v for v in g.nodes() if g.degree(v) % 2 != 0}
        assert {path[0], path[-1]} == odd_vertices


# ---------------------------------------------------------------------------
# NEGATIVE scenario tests (no Euler path)
# ---------------------------------------------------------------------------
class TestFleuryNegative:
    """Graphs that do NOT have an Euler path → ValueError expected."""

    def test_disconnected_graph(self):
        """Two separate edges 1-2 and 3-4 → disconnected, no Euler path."""
        g = nx.Graph([(1, 2), (3, 4)])
        with pytest.raises(ValueError, match="does not have an Euler path"):
            find_euler_path(g)

    def test_complete_k4_four_odd_vertices(self):
        """Complete K₄ → all 4 vertices have degree 3 (odd) → no Euler path."""
        g = nx.Graph([(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)])
        with pytest.raises(ValueError, match="does not have an Euler path"):
            find_euler_path(g)

    def test_empty_graph_no_edges(self):
        """Graph with vertices but no edges → no Euler path."""
        g = nx.Graph()
        g.add_nodes_from([1, 2, 3])
        with pytest.raises(ValueError, match="does not have an Euler path"):
            find_euler_path(g)

    def test_single_vertex_no_edges(self):
        """Single vertex without edges → no Euler path."""
        g = nx.Graph()
        g.add_node(1)
        with pytest.raises(ValueError, match="does not have an Euler path"):
            find_euler_path(g)


# ---------------------------------------------------------------------------
# Bridge logic tests (specific to Fleury's algorithm)
# ---------------------------------------------------------------------------
class TestFleuryBridgeLogic:
    """Tests that specifically exercise Fleury's bridge detection logic.

    Fleury avoids crossing bridge edges when non-bridge alternatives exist.
    """

    def test_is_bridge_on_longer_chain(self):
        """In chain 1-2-3-4, edge (2,3) is a bridge (disconnects two components with edges)."""
        g = nx.Graph([(1, 2), (2, 3), (3, 4)])
        assert _is_bridge(g, 2, 3) is True

    def test_is_not_bridge_in_triangle(self):
        """In a triangle 1-2-3, no edge is a bridge."""
        g = nx.Graph([(1, 2), (2, 3), (3, 1)])
        assert _is_bridge(g, 1, 2) is False

    def test_figure_eight_bridge_at_center(self):
        """Figure-8: two triangles sharing vertex 1.

        All even degrees → Euler circuit.
        Fleury must navigate through center vertex correctly.
        """
        g = nx.Graph([(1, 2), (2, 3), (3, 1), (1, 4), (4, 5), (5, 1)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        assert path[0] == path[-1]

    def test_lollipop_graph(self):
        """Lollipop: triangle 1-2-3 with chain 3-4-5 → bridge at edge 3-4.

        Vertices 1 and 5 have odd degree → Euler path exists.
        Fleury must navigate bridge at 3-4 correctly.
        """
        g = nx.Graph([(1, 2), (2, 3), (3, 1), (3, 4), (4, 5)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)

    def test_bridge_is_only_option(self):
        """When only one neighbor exists, Fleury must take the bridge.

        Chain 1-2-3 → every edge is a bridge.
        """
        g = nx.Graph([(1, 2), (2, 3)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        assert len(path) == 3


# ---------------------------------------------------------------------------
# Large / complex graph tests
# ---------------------------------------------------------------------------
class TestFleuryLargeGraphs:
    """Tests on larger graphs to verify algorithm scalability."""

    def test_large_ring_circuit_20_nodes(self):
        """Ring of 20 nodes → 20 edges, Euler circuit."""
        n = 20
        g = nx.Graph()
        for i in range(n):
            g.add_edge(i, (i + 1) % n)
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        assert path[0] == path[-1]
        assert len(path) == n + 1

    def test_large_chain_path_10_nodes(self):
        """Chain of 10 nodes → 9 edges, Euler path."""
        n = 10
        g = nx.Graph()
        for i in range(n - 1):
            g.add_edge(i, i + 1)
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        assert len(path) == n


# ---------------------------------------------------------------------------
# Immutability test
# ---------------------------------------------------------------------------
class TestFleuryImmutability:
    """Algorithm must not modify the original graph."""

    def test_does_not_mutate_circuit_graph(self):
        """After running on circuit graph, the original must remain unchanged."""
        g = nx.Graph([(1, 2), (2, 3), (3, 1)])
        original_nodes = set(g.nodes())
        original_edges = set(g.edges())
        find_euler_path(g)
        assert set(g.nodes()) == original_nodes
        assert set(g.edges()) == original_edges

    def test_does_not_mutate_path_graph(self):
        """After running on path graph, the original must remain unchanged."""
        g = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 2)])
        original_nodes = set(g.nodes())
        original_edges = set(g.edges())
        find_euler_path(g)
        assert set(g.nodes()) == original_nodes
        assert set(g.edges()) == original_edges


# ---------------------------------------------------------------------------
# Mutation-targeted tests (kill surviving MutPy mutants)
# ---------------------------------------------------------------------------
class TestFleuryMutationTargets:
    """Tests designed to kill specific surviving MutPy mutants.

    Each test documents the mutant it targets, identified by
    mutation operator and line-level description.
    """

    def test_single_neighbor_branch(self):
        """Kill mutant #15/#28 (COI/ROR): len(neighbors)==1 inversion.

        In a chain 1-2-3, vertex 2 always has exactly 1 neighbor after
        removing the first edge. If the single-neighbor branch is swapped,
        the algorithm enters multi-neighbor logic for a 1-neighbor case.
        """
        g = nx.Graph([(1, 2), (2, 3)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        assert len(path) == 3

    def test_bridge_or_condition_in_is_bridge(self):
        """Kill mutant #21 (LCR): `or` → `and` in _is_bridge.

        In chain 1-2-3, removing edge (1,2) makes vertex 1 isolated
        while vertex 2 still has edges. With `or`, the elif triggers
        (u not in vertices_with_edges). With `and`, both would need
        to be missing, so it falls through to the else branch.
        """
        g = nx.Graph([(1, 2), (2, 3)])
        # Edge (1,2) is a bridge
        assert _is_bridge(g, 1, 2) is True
        # Verify graph is restored after bridge check
        assert g.has_edge(1, 2)

    def test_bridge_check_one_vertex_isolated(self):
        """Kill mutant #21 (LCR): specifically test case where exactly
        one vertex becomes isolated after edge removal.

        Graph: 1-2-3-4 (chain). Remove edge (1,2) → vertex 1 has
        degree 0, vertex 2 still has edges. The `or` detects this,
        while `and` would miss it.
        """
        g = nx.Graph([(1, 2), (2, 3), (3, 4)])
        result = _is_bridge(g, 1, 2)
        # After removing (1,2), vertex 1 is isolated, vertices 2,3,4 still connected
        # _is_bridge returns True (it disconnected the graph)
        assert result is True
        assert g.has_edge(1, 2)

    def test_fleury_on_diamond_with_tail(self):
        """Kill mutant #17 (COI): next_vertex is None fallback.

        Diamond 1-2-3 with edges 1-3 plus tail 3-4.
        Multiple neighbors = bridge detection + fallback logic.
        """
        g = nx.Graph([(1, 2), (2, 3), (1, 3), (3, 4)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)

    def test_cleanup_logic_on_pentagon(self):
        """Kill mutant #30 (ROR): current==next_vertex cleanup check.

        Pentagon graph exercises node removal cleanup at each step.
        """
        g = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        assert path[0] == path[-1]

    def test_all_bridges_graph(self):
        """Kill mutant #1 (BCR): break→continue in `if not neighbors`.

        Star graph: 1 connected to 2, 3, 4 each with one extra edge.
        After processing, isolated vertices may trigger infinite loop
        if `break` is replaced by `continue`.
        """
        g = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 1)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)

    def test_complex_bridge_multi_component(self):
        """Kill mutants related to bridge detection with complex topology.

        Bowtie graph: triangles 1-2-3 and 3-4-5 sharing vertex 3.
        Vertex 3 has degree 4 (even), all others degree 2. Euler circuit.
        """
        g = nx.Graph([(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 3)])
        path = find_euler_path(g)
        assert _is_valid_euler_path(g, path)
        assert path[0] == path[-1]

