import sys
import threading
import types

# Monkey-patching MutPy for Python 3.9+ compatibility
# threading.Thread.isAlive was removed in Python 3.9
if not hasattr(threading.Thread, 'isAlive'):
    threading.Thread.isAlive = threading.Thread.is_alive

from mutpy import commandline

if __name__ == "__main__":
    commandline.main(sys.argv)
