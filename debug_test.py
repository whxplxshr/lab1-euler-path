
import sys
import os
sys.path.append(os.getcwd())

import networkx as nx
import pytest
from src.graph_utils import has_euler_path, has_euler_circuit, get_euler_start_vertex
from tests.test_bva import TestGraphUtilsBVA


def run_debug():
    print("Running TestGraphUtilsBVA...")

    with open("debug_output.txt", "w") as f:
        f.write("Running TestGraphUtilsBVA...\n")
        t = TestGraphUtilsBVA()
        
        try:
            f.write("Running test_bva_zero_nodes...\n")
            t.test_bva_zero_nodes()
            f.write("PASS\n")
        except Exception as e:
            f.write(f"FAIL: {e}\n")
            import traceback
            traceback.print_exc(file=f)

        try:
            f.write("Running test_bva_one_node_zero_edges...\n")
            t.test_bva_one_node_zero_edges()
            f.write("PASS\n")

        except Exception as e:
            f.write(f"FAIL: {e}\n")
            import traceback
            traceback.print_exc(file=f)

    print("Running TestAlgorithmsBVA...")
    from src.hierholzer import find_euler_path as hierholzer_find
    from src.fleury import find_euler_path as fleury_find
    from tests.test_bva import TestAlgorithmsBVA

    # TestAlgorithmsBVA needs algo_find parametrization. We'll run manual content.
    t_algo = TestAlgorithmsBVA()
    
    for algo_name, algo_func in [("Hierholzer", hierholzer_find), ("Fleury", fleury_find)]:
        with open("debug_output.txt", "a") as f:
            f.write(f"\nTesting {algo_name}...\n")
        
        try:
            with open("debug_output.txt", "a") as f: f.write("  test_bva_min_path_1_edge... ")
            t_algo.test_bva_min_path_1_edge(algo_func)
            with open("debug_output.txt", "a") as f: f.write("PASS\n")
        except Exception as e:
             with open("debug_output.txt", "a") as f: 
                f.write(f"FAIL: {e}\n")
                import traceback
                traceback.print_exc(file=f)

        try:
            with open("debug_output.txt", "a") as f: f.write("  test_bva_min_circuit_triangle... ")
            t_algo.test_bva_min_circuit_triangle(algo_func)
            with open("debug_output.txt", "a") as f: f.write("PASS\n")
        except Exception as e:
             with open("debug_output.txt", "a") as f: 
                f.write(f"FAIL: {e}\n")
                import traceback
                traceback.print_exc(file=f)

        try:
             with open("debug_output.txt", "a") as f: f.write("  test_bva_disconnected_with_edges... ")
             # This test expects pytest.raises. We need to simulate it or wrap it.
             # But the test method uses `with pytest.raises(...)`. 
             # So we can just call it? Yes, if pytest is imported and handles it.
             # Wait, TestAlgorithmsBVA uses `pytest.raises`. 
             # Standard pytest.raises works as context manager.
             t_algo.test_bva_disconnected_with_edges(algo_func)
             with open("debug_output.txt", "a") as f: f.write("PASS\n")
        except Exception as e:
             with open("debug_output.txt", "a") as f: 
                f.write(f"FAIL: {e}\n")
                import traceback
                traceback.print_exc(file=f)



    print("Running TestIOHandlerBVA...")
    from tests.test_bva import TestIOHandlerBVA
    t_io = TestIOHandlerBVA()

    # We need tmp_path fixture. We can simulate it using tempfile.
    import tempfile
    import shutil
    import pathlib

    with open("debug_output.txt", "a") as f:
        f.write("\nTesting IOHandler...\n")

    # Helper for tmp_path
    class MockTmpPath:
        def __init__(self):
            self.dir = tempfile.mkdtemp()
            self.path = pathlib.Path(self.dir)
        def cleanup(self):
            shutil.rmtree(self.dir)
    
    tmp = MockTmpPath()
    try:
        try:
            with open("debug_output.txt", "a") as f: f.write("  test_bva_load_empty_json_object... ")
            t_io.test_bva_load_empty_json_object(tmp.path)
            with open("debug_output.txt", "a") as f: f.write("PASS\n")
        except Exception as e:
                with open("debug_output.txt", "a") as f: 
                    f.write(f"FAIL: {e}\n")
                    import traceback
                    traceback.print_exc(file=f)

        try:
            with open("debug_output.txt", "a") as f: f.write("  test_bva_load_empty_lists... ")
            t_io.test_bva_load_empty_lists(tmp.path)
            with open("debug_output.txt", "a") as f: f.write("PASS\n")
        except Exception as e:
                with open("debug_output.txt", "a") as f: 
                    f.write(f"FAIL: {e}\n")
                    import traceback
                    traceback.print_exc(file=f)
        
        try:
            with open("debug_output.txt", "a") as f: f.write("  test_bva_load_single_vertex_no_edges... ")
            t_io.test_bva_load_single_vertex_no_edges(tmp.path)
            with open("debug_output.txt", "a") as f: f.write("PASS\n")
        except Exception as e:
                with open("debug_output.txt", "a") as f: 
                    f.write(f"FAIL: {e}\n")
                    import traceback
                    traceback.print_exc(file=f)

        try:
            with open("debug_output.txt", "a") as f: f.write("  test_bva_save_single_node_path... ")
            t_io.test_bva_save_single_node_path(tmp.path)
            with open("debug_output.txt", "a") as f: f.write("PASS\n")
        except Exception as e:
                with open("debug_output.txt", "a") as f: 
                    f.write(f"FAIL: {e}\n")
                    import traceback
                    traceback.print_exc(file=f)

        try:
            with open("debug_output.txt", "a") as f: f.write("  test_bva_save_empty_algo_name... ")
            t_io.test_bva_save_empty_algo_name(tmp.path)
            with open("debug_output.txt", "a") as f: f.write("PASS\n")
        except Exception as e:
                with open("debug_output.txt", "a") as f: 
                    f.write(f"FAIL: {e}\n")
                    import traceback
                    traceback.print_exc(file=f)



    finally:
        tmp.cleanup()

    print("Running TestConsoleInputBVA...")
    from tests.test_bva import TestConsoleInputBVA
    t_console = TestConsoleInputBVA()
    
    with open("debug_output.txt", "a") as f:
        f.write("\nTesting ConsoleInputBVA...\n")

    try:
        with open("debug_output.txt", "a") as f: f.write("  test_bva_zero_vertices... ")
        # patch decorator makes it callable but we need to ensure patch is active?
        # When calling instance method decorated with patch, it works.
        t_console.test_bva_zero_vertices()
        with open("debug_output.txt", "a") as f: f.write("PASS\n")
    except Exception as e:
            with open("debug_output.txt", "a") as f: 
                f.write(f"FAIL: {e}\n")
                import traceback
                traceback.print_exc(file=f)

    try:
        with open("debug_output.txt", "a") as f: f.write("  test_bva_one_vertex_zero_edges... ")
        t_console.test_bva_one_vertex_zero_edges()
        with open("debug_output.txt", "a") as f: f.write("PASS\n")
    except Exception as e:
            with open("debug_output.txt", "a") as f: 
                f.write(f"FAIL: {e}\n")
                import traceback
                traceback.print_exc(file=f)

    try:
        with open("debug_output.txt", "a") as f: f.write("  test_bva_min_valid_edge_input... ")
        t_console.test_bva_min_valid_edge_input()
        with open("debug_output.txt", "a") as f: f.write("PASS\n")
    except Exception as e:
            with open("debug_output.txt", "a") as f: 
                f.write(f"FAIL: {e}\n")
                import traceback
                traceback.print_exc(file=f)

if __name__ == "__main__":
    try:
        os.remove("debug_output.txt")
    except FileNotFoundError:
        pass
    run_debug()

