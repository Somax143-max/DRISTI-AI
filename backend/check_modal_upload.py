import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('portal_engine.js', 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()

idx = text.find('function handleModalCustomUpload')
if idx != -1:
    print(text[idx:idx+450])
else:
    print('handleModalCustomUpload not found')
