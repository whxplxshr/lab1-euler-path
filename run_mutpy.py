"""MutPy runner script for Windows + Python 3.9.

Usage:
    py -3.9 run_mutpy.py --target src.module_name --unit-test tests.test_module [tests.test_other]

MutPy 0.6.1 requires Python <=3.9 and has two compatibility issues:
1. Cannot be invoked via `python -m mutpy` — must call commandline.main() directly.
2. Uses deprecated threading.Thread.isAlive() which was removed in Python 3.9.
"""

import sys
import threading

# Patch: threading.Thread.isAlive was removed in Python 3.9,
# but MutPy still references it internally.
if not hasattr(threading.Thread, "isAlive"):
    threading.Thread.isAlive = threading.Thread.is_alive

from mutpy import commandline


if __name__ == "__main__":
    sys.exit(commandline.main(argv=sys.argv[1:]))
