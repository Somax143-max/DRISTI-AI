import re
with open('create_realtime_portal.py', 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()

ids = set(re.findall(r'id=["\']([^"\']+)["\']', text))
handlers = set(re.findall(r'on\w+=["\']([^"\']+)["\']', text))

print('Found IDs count:', len(ids))
print('IDs:', sorted(list(ids)))
print('\nHandlers count:', len(handlers))
print('Handlers:', sorted(list(handlers)))
