"""Batch runner: runs MutPy on all source modules and saves logs."""

import subprocess
import sys

PYTHON = sys.executable  # Python 3.9

RUNS = [
    {
        "name": "fleury",
        "args": ["--target", "src.fleury", "--unit-test", "tests.test_fleury", "--runner", "pytest"],
    },
    {
        "name": "io_handler",
        "args": ["--target", "src.io_handler", "--unit-test", "tests.test_io_handler", "--runner", "pytest"],
    },
    {
        "name": "console_input",
        "args": ["--target", "src.console_input", "--unit-test", "tests.test_console_input", "--runner", "pytest"],
    },
]

for run in RUNS:
    name = run["name"]
    print(f"\n{'='*60}")
    print(f"  Running MutPy on: {name}")
    print(f"{'='*60}")

    cmd = [PYTHON, "run_mutpy.py"] + run["args"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    output = result.stdout + result.stderr
    log_path = f"mutpy_{name}.log"

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(output)

    print(output)
    print(f"  -> Saved to {log_path}")
