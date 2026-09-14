import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('web/index.html', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

for i in range(468, 496):
    print(f'{i+1}: {lines[i]}', end='')
