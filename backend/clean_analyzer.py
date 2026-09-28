with open("retina_analyzer.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Remove test execution lines at the bottom of module
clean_lines = []
for l in lines:
    if "user_img = cv2.imread(" in l or "res = analyze_retinal_fundus(" in l or "--- UPDATED ANALYZER" in l:
        break
    clean_lines.append(l)

with open("retina_analyzer.py", "w", encoding="utf-8") as f:
    f.writelines(clean_lines)

print(f"retina_analyzer.py cleaned! Total lines: {len(clean_lines)}")
