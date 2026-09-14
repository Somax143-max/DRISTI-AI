import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('create_realtime_portal.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'view-field' in l or 'view-clinical' in l or 'view-admin' in l:
        print(f"{i+1}: {l.strip()[:100]}")
