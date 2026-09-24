import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('portal_engine.js', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function handleFileUpload' in l or 'function updateRealtimeCanvas' in l:
        print(f"Line {i+1}: {l.strip()}")
