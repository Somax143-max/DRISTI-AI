with open('web/index.html', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '.modal {' in l:
        for j in range(i, min(i+25, len(lines))):
            print(lines[j], end='')
        break
