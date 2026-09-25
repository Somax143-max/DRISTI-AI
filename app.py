import os
import sys

# Ensure server package is on python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_DIR = os.path.join(BASE_DIR, 'server')
if SERVER_DIR not in sys.path:
    sys.path.insert(0, SERVER_DIR)

# Prevent Windows OS from sleeping if run locally
try:
    if os.name == 'nt':
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000041)
except Exception:
    pass

from server import run_server

if __name__ == '__main__':
    # Cloud environments (Hugging Face / Render) provide PORT via environment variable
    port = int(os.environ.get('PORT', sys.argv[1] if len(sys.argv) > 1 else 7860))
    run_server(port)
