with open('web/index.html', 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()

print('Has reportModal?', 'id="reportModal"' in text)
for l in text.splitlines():
    if '.modal' in l:
        print(l.strip()[:100])
