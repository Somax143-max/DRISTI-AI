import cv2
import numpy as np

img_path = r'C:/Users/DELL/.gemini/antigravity/brain/83a8594b-73c9-401b-8ba6-024177eb2f1c/.user_uploaded/media_1788888654346.png'
img = cv2.imread(img_path)
h, w = img.shape[:2]

r = img[:, :, 2].astype(float)
g = img[:, :, 1].astype(float)
b = img[:, :, 0].astype(float)

retina_mask = ((r - b) > 35).astype(np.uint8) * 255
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
retina_mask = cv2.morphologyEx(retina_mask, cv2.MORPH_CLOSE, k)
retina_mask = cv2.morphologyEx(retina_mask, cv2.MORPH_OPEN, k)

contours, _ = cv2.findContours(retina_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
largest_cnt = max(contours, key=cv2.contourArea)
(cx, cy), radius = cv2.minEnclosingCircle(largest_cnt)
cx, cy, radius = int(cx), int(cy), int(radius)

# Crop bounding box around retinal circle with a small margin
x1 = max(0, cx - radius)
x2 = min(w, cx + radius)
y1 = max(0, cy - radius)
y2 = min(h, cy + radius)

retina_crop = img[y1:y2, x1:x2]
print(f"Cropped Retina Shape: {retina_crop.shape}")

# Resize cropped retina to standardized 512x512 for medical-grade analysis
retina_std = cv2.resize(retina_crop, (512, 512), interpolation=cv2.INTER_CUBIC)
cv2.imwrite("user_retina_isolated.png", retina_std)

# Run lesion detection on the isolated retina!
import retina_analyzer
res = retina_analyzer.analyze_retinal_fundus(retina_std)
print("\n--- ANALYSIS OF USER'S CROPPED RETINA ---")
print("Verified Retina?", res["verified_retina"])
if res["verified_retina"]:
    print(f"Diagnostic Staging: {res['grade_name']}")
    print(f"Referable DR Status: {res['ref_title']}")
    print(f"Microaneurysms: {res['mas_count']}")
    print(f"Hemorrhages: {res['hemo_count']}")
    print(f"Exudates: {res['exudates_count']}")
    print(f"CSME Positive: {res['csme_positive']} (Distance: {res['csme_dist_dd']} DD)")
    print(f"Vessel Density: {res['vessel_density_pct']}%")
