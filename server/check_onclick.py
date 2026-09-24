with open('create_realtime_portal.py', 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()

import re
matches = re.findall(r'onclick=[\"\']([^\"\']+)[\"\']', text)
for m in set(matches):
    print(m)
