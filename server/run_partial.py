with open('create_realtime_portal.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Execute up to where it currently is
scope = {}
exec(code, scope)
html_so_far = "".join(scope['html_parts'])
print("HTML so far length:", len(html_so_far))
with open('web/index.html', 'w', encoding='utf-8') as f:
    f.write(html_so_far)
print("web/index.html written successfully with partial HTML.")
