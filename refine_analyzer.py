with open('retina_analyzer.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace MA loop
old_loop = """    for i in range(1, num_d):
        area = stats_d[i, cv2.CC_STAT_AREA]
        cx, cy = int(centroids_d[i][0]), int(centroids_d[i][1])
        # Circularity filter
        comp_mask = (labels_d == i).astype(np.uint8)
        contours, _ = cv2.findContours(comp_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours: continue
        cnt = contours[0]
        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0: continue
        circularity = 4 * np.pi * (area / (perimeter * perimeter))
        
        if 2 <= area <= 35 and circularity > 0.45:
            mas_coords.append({"x": cx, "y": cy, "r": 3})
        elif 35 < area <= 800:
            hemo_coords.append({"x": cx, "y": cy, "r": max(3, int(np.sqrt(area/np.pi)))})"""

new_loop = """    for i in range(1, num_d):
        area = stats_d[i, cv2.CC_STAT_AREA]
        cx, cy = int(centroids_d[i][0]), int(centroids_d[i][1])
        if cx < 6 or cx >= w - 6 or cy < 6 or cy >= h - 6:
            continue
            
        local_center = np.mean(g_clahe[cy-1:cy+2, cx-1:cx+2])
        ring_mask = np.zeros((13, 13), dtype=np.uint8)
        cv2.circle(ring_mask, (6, 6), 6, 255, -1)
        cv2.circle(ring_mask, (6, 6), 3, 0, -1)
        local_patch = g_clahe[cy-6:cy+7, cx-6:cx+7]
        local_bg = np.mean(local_patch[ring_mask > 0])
        contrast = local_bg - local_center
        
        if 3 <= area <= 40 and contrast > 18:
            mas_coords.append({"x": cx, "y": cy, "r": 3})
        elif 40 < area <= 800 and contrast > 15:
            hemo_coords.append({"x": cx, "y": cy, "r": max(3, int(np.sqrt(area/np.pi)))})"""

if old_loop in code:
    code = code.replace(old_loop, new_loop)
    with open('retina_analyzer.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("retina_analyzer.py updated with clinical contrast-filtered MA extraction.")
else:
    print("Pattern not found in retina_analyzer.py.")
