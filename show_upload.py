import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('portal_engine.js', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

for i in range(500, min(590, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')
