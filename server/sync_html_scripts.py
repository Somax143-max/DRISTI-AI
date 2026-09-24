import sys

with open("portal_engine.js", "r", encoding="utf-8") as f:
    js_code = f.read()

for path in ["web/index.html", "index.html"]:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
        
    s_idx = html.find("<script>")
    e_idx = html.find("</script>")
    if s_idx != -1 and e_idx != -1:
        new_html = html[:s_idx + len("<script>")] + "\n" + js_code + "\n    " + html[e_idx:]
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"Updated {path} ({len(new_html):,} bytes)")
    else:
        print(f"Could not find script block in {path}")
