import os
import shutil

# 1. Read HTML base
with open('web/index.html', 'r', encoding='utf-8') as f:
    html_base = f.read()

# 2. Read JS engine
with open('portal_engine.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

# 3. Copy external JS to web directory as well
os.makedirs('web', exist_ok=True)
shutil.copyfile('portal_engine.js', 'web/portal_engine.js')
print("Copied portal_engine.js to web/portal_engine.js")

# 4. Create fully self-contained HTML (inline script for maximum portability)
final_html = html_base + "\n    <script>\n" + js_code + "\n    </script>\n</body>\n</html>\n"

# 5. Write to web/index.html and root index.html
with open('web/index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("SUCCESS: web/index.html and index.html generated!")
print(f"Final file size: {len(final_html):,} bytes ({len(final_html.splitlines())} lines)")
