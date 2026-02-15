import sys
from unittest.mock import MagicMock
import multiprocessing

# 1. Mock resource (Unix only)
sys.modules['resource'] = MagicMock()

# 2. Patch multiprocessing to use 'spawn' on Windows
# This is crucial because mutmut defaults to 'fork' which is Unix-only
try:
    if sys.platform.startswith('win'):
        multiprocessing.set_start_method('spawn', force=True)
except RuntimeError:
    pass

# Import mutmut
try:
    from mutmut.__main__ import main
except ImportError:
    try:
        from mutmut import main
    except ImportError:
        print("Error: Could not import 'main' from mutmut.")
        sys.exit(1)

if __name__ == '__main__':
    # Add froze_suppport for Windows executables (good practice)
    multiprocessing.freeze_support()
    try:
        main()
    except Exception as e:
        print(f"mutmut crashed: {e}")
        import traceback
        traceback.print_exc()
