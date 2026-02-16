
import os
import shutil
import glob
from pathlib import Path

# Directories to remove
dirs = [".pytest_cache", "htmlcov", ".mutmut-cache"]
for d in dirs:
    if os.path.exists(d):
        try:
            shutil.rmtree(d, ignore_errors=True)
            print(f"Removed directory: {d}")
        except Exception as e:
            print(f"Error removing {d}: {e}")

# Recursive __pycache__
for p in Path(".").rglob("__pycache__"):
    try:
        shutil.rmtree(p, ignore_errors=True)
        print(f"Removed directory: {p}")
    except Exception as e:
        print(f"Error removing {p}: {e}")

# Files to remove pattern-based
patterns = [
    "*.log",
    "debug_*.txt",
    "debug_*.py",
    "run_*.py",
    "test_output.txt",
    "test_run.txt",
    "test_results.txt",
    "fleury_results.txt",
    "coverage_report.txt",
    "test_output.log",
    "full_test_log.txt",
    "repro_fail.py",
    "run_tests.bat",
    "requirements_dev.txt"  # If exists and not needed? No keep requirements.txt
]

for pattern in patterns:
    for f in glob.glob(pattern):
        if f == "cleanup.py": continue
        try:
            os.remove(f)
            print(f"Deleted file: {f}")
        except OSError as e:
            print(f"Error deleting {f}: {e}")

print("Cleanup complete.")
