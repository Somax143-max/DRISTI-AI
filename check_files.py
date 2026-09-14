# Verify Python is ready
import os
print("Current files:", [f for f in os.listdir('.') if f.endswith('.html') or f.endswith('.js')])
