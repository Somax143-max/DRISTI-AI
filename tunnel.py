import os
import subprocess
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
exe_path = os.path.join(BASE_DIR, 'cloudflared.exe')

# Fallbacks if not in project folder
if not os.path.exists(exe_path):
    alt_path = r'C:\Program Files (x86)\cloudflared\cloudflared.exe'
    if os.path.exists(alt_path):
        exe_path = alt_path
    else:
        exe_path = 'cloudflared'

port = sys.argv[1] if len(sys.argv) > 1 else '8081'

print("=" * 65)
print(f"  Starting DRISHTI-AI Public Cloudflare Tunnel for Port {port}...")
print("=" * 65)
print("\nConnecting to Cloudflare network, please wait a moment...\n")

cmd = [exe_path, 'tunnel', '--url', f'http://localhost:{port}']

try:
    process = subprocess.Popen(
        cmd,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
except Exception as e:
    print(f"Error launching {exe_path}: {e}")
    sys.exit(1)

url_found = False
for line in iter(process.stderr.readline, ''):
    # Search for trycloudflare.com URL
    match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
    if match and not url_found:
        url_found = True
        public_url = match.group(0)
        print("=" * 65)
        print("  [SUCCESS] YOUR PUBLIC HACKATHON DEMO URL IS READY:")
        print(f"  --> {public_url}")
        print("=" * 65)
        print("\nShare this link with judges! Keep this window open.")
        print("(Press Ctrl + C in this window to stop the tunnel)\n")
        sys.stdout.flush()
    elif not url_found and 'Requesting new quick Tunnel' in line:
        print("Allocating public tunnel address...")
        sys.stdout.flush()

process.wait()
