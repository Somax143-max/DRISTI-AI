import re

with open('web/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all document.getElementById calls in JS
dom_gets = set(re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", html))
# Find all id="..." in HTML
defined_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))

missing = dom_gets - defined_ids
print("Total getElementById queries:", len(dom_gets))
print("Total defined HTML IDs:", len(defined_ids))
print("Missing IDs count:", len(missing))
if missing:
    print("Missing IDs:", missing)
else:
    print("PERFECT: 100% of DOM queries match existing HTML element IDs!")
