import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('create_realtime_portal.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

print("Lines around canvas and controls in view-clinical:")
for i in range(498, 560):
    print(f"{i+1}: {lines[i]}", end='')
