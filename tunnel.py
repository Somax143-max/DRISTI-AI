import os
import shutil
import subprocess
import sys
import re
import urllib.request
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def prevent_windows_sleep():
    """Instructs Windows kernel to never sleep while this process is alive."""
    if os.name == 'nt':
        try:
            import ctypes
            # ES_CONTINUOUS (0x80000000) | ES_SYSTEM_REQUIRED (0x00000001) | ES_AWAYMODE_REQUIRED (0x00000040)
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000041)
            print("  [AWAKE] Windows 10 sleep mode is actively blocked (Never-Sleep Active).")
        except Exception:
            pass

def get_cloudflared_path():
    candidates = [
        os.path.join(BASE_DIR, 'cloudflared.exe'),
        os.path.join(BASE_DIR, 'cloudflare.exe'),
        r'C:\Program Files (x86)\cloudflared\cloudflared.exe',
        r'C:\Program Files\cloudflared\cloudflared.exe',
        os.path.expandvars(r'%LOCALAPPDATA%\Programs\Python\Python314\Scripts\cloudflared.exe'),
        os.path.expandvars(r'%LOCALAPPDATA%\Programs\Python\Python314\Scripts\cloudflare.exe'),
        os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\WindowsApps\cloudflared.exe'),
        os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\WindowsApps\cloudflare.exe'),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return os.path.abspath(c)

    # Check PATH using shutil.which
    for name in ['cloudflared', 'cloudflare']:
        w = shutil.which(name)
        if w and w.lower().endswith('.exe') and os.path.isfile(w):
            return os.path.abspath(w)

    # If not found anywhere, auto-download official Cloudflare executable
    target_path = os.path.join(BASE_DIR, 'cloudflared.exe')
    print("=" * 65)
    print("  cloudflared.exe not found locally.")
    print("  Downloading official Cloudflare tunnel binary (~50MB)...")
    print("  This is a one-time automatic setup for your PC.")
    print("=" * 65)
    url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    try:
        def reporthook(count, block_size, total_size):
            if total_size > 0:
                percent = int(count * block_size * 100 / total_size)
                sys.stdout.write(f"\r  Downloading: {min(percent, 100)}% complete...")
                sys.stdout.flush()
        urllib.request.urlretrieve(url, target_path, reporthook=reporthook)
        print("\n  [SUCCESS] cloudflared.exe downloaded successfully!\n")
        return target_path
    except Exception as err:
        print(f"\n  [ERROR] Failed to download cloudflared.exe: {err}")
        return None

def start_tunnel():
    port = sys.argv[1] if len(sys.argv) > 1 else '8081'
    exe_path = get_cloudflared_path()
    
    if not exe_path or not os.path.isfile(exe_path):
        print("=" * 65)
        print("  [ERROR] Could not locate or download cloudflared.exe")
        print("  Please manually download cloudflared-windows-amd64.exe from:")
        print("  https://github.com/cloudflare/cloudflared/releases/latest")
        print("  and save it as 'cloudflared.exe' in this project folder.")
        print("=" * 65)
        sys.exit(1)

    prevent_windows_sleep()

    while True:
        print("=" * 65)
        print(f"  Starting DRISHTI-AI Public Cloudflare Tunnel for Port {port}...")
        print(f"  Binary: {exe_path}")
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
            match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
            if match and not url_found:
                url_found = True
                public_url = match.group(0)
                try:
                    with open(os.path.join(BASE_DIR, 'latest_public_url.txt'), 'w', encoding='utf-8') as f:
                        f.write(public_url + '\n')
                except Exception:
                    pass
                print("=" * 65)
                print("  [SUCCESS] YOUR PUBLIC HACKATHON DEMO URL IS READY:")
                print(f"  --> {public_url}")
                print("=" * 65)
                print(f"\n[SAVED] Link written to latest_public_url.txt")
                print("Share this link with judges! Keep this window open.")
                print("(Press Ctrl + C in this window to stop the tunnel)\n")
                sys.stdout.flush()
            elif not url_found and 'Requesting new quick Tunnel' in line:
                print("Allocating public tunnel address...")
                sys.stdout.flush()

        process.wait()
        print("\n[WATCHDOG] Connection dropped or interrupted. Auto-reconnecting in 3 seconds...\n")
        time.sleep(3)

if __name__ == '__main__':
    start_tunnel()
