import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('create_realtime_portal.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

for i in range(472, 497):
    print(f"{i+1}: {lines[i]}", end='')
