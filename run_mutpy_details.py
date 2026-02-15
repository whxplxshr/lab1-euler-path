"""Show surviving mutant details for modules with surviving mutants."""

import subprocess
import sys

PYTHON = sys.executable

RUNS = [
    {
        "name": "graph_utils",
        "args": ["--target", "src.graph_utils", "--unit-test", "tests.test_graph_utils", "tests.test_bva",
                 "--runner", "pytest", "--show-mutants"],
    },
    {
        "name": "fleury",
        "args": ["--target", "src.fleury", "--unit-test", "tests.test_fleury",
                 "--runner", "pytest", "--show-mutants"],
    },
    {
        "name": "io_handler",
        "args": ["--target", "src.io_handler", "--unit-test", "tests.test_io_handler",
                 "--runner", "pytest", "--show-mutants"],
    },
]

for run in RUNS:
    name = run["name"]
    cmd = [PYTHON, "run_mutpy.py"] + run["args"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    output = result.stdout + result.stderr
    log_path = f"mutpy_{name}_details.log"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"  -> {name}: saved to {log_path}")
