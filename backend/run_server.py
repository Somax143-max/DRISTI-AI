import os
import sys

# Ensure backend package is on python path
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Prevent Windows OS from sleeping while server is running
if os.name == 'nt':
    try:
        import ctypes
        # ES_CONTINUOUS (0x80000000) | ES_SYSTEM_REQUIRED (0x00000001) | ES_AWAYMODE_REQUIRED (0x00000040)
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000041)
    except Exception:
        pass

from server import run_server

if __name__ == '__main__':
    port = int(os.environ.get('PORT', sys.argv[1] if len(sys.argv) > 1 else 8081))
    run_server(port)
