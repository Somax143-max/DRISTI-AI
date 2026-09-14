try:
    with open('create_realtime_portal.py', 'r', encoding='utf-8') as f:
        code = f.read()
    print("Script character length:", len(code))
    # Test if it compiles
    compile(code, 'create_realtime_portal.py', 'exec')
    print("create_realtime_portal.py compiles successfully!")
except Exception as e:
    print("Error:", e)
