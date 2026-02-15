"""Run targeted fleury tests and capture output."""
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_fleury.py", "-v", "--tb=long"],
    capture_output=True, text=True, timeout=30
)
with open("test_debug_output.txt", "w", encoding="utf-8") as f:
    f.write(result.stdout)
    f.write(result.stderr)
print("Done, exit code:", result.returncode)
