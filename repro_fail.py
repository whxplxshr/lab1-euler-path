
import networkx as nx
import sys
import os
sys.path.append(os.getcwd())
from src.graph_utils import has_euler_path, has_euler_circuit, get_euler_start_vertex

def test():
    print("Testing zero nodes graph...")
    g = nx.Graph()
    
    res_path = has_euler_path(g)
    print(f"has_euler_path(g) = {res_path}")
    if res_path is not False:
        print("FAIL: has_euler_path should be False")
        exit(1)
        
    res_circuit = has_euler_circuit(g)
    print(f"has_euler_circuit(g) = {res_circuit}")
    if res_circuit is not False:
        print("FAIL: has_euler_circuit should be False")
        exit(1)

    try:
        get_euler_start_vertex(g)
        print("FAIL: get_euler_start_vertex should raise ValueError")
        exit(1)
    except ValueError as e:
        print(f"Caught expected error: {e}")
        if "no Euler path" not in str(e):
             print(f"FAIL: Error message mismatch. Got '{e}'")
             exit(1)
    except Exception as e:
        print(f"FAIL: Caught unexpected error: {type(e)} {e}")
        exit(1)
    
    print("PASS")

if __name__ == "__main__":
    test()
