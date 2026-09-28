import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
SERVER_DIR = os.path.join(BASE_DIR, 'server')

# Priority: backend directory, fallback to server
if os.path.isdir(BACKEND_DIR) and BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
elif os.path.isdir(SERVER_DIR) and SERVER_DIR not in sys.path:
    sys.path.insert(0, SERVER_DIR)

# Prevent Windows OS from sleeping while server is running
if os.name == 'nt':
    try:
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000041)
    except Exception:
        pass

from server import run_server

if __name__ == '__main__':
    port = int(os.environ.get('PORT', sys.argv[1] if len(sys.argv) > 1 else 8081))
    run_server(port)
