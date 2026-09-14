import cv2
import numpy as np

img_path = r'C:/Users/DELL/.gemini/antigravity/brain/83a8594b-73c9-401b-8ba6-024177eb2f1c/.user_uploaded/media_1788888654346.png'
img_bgr = cv2.imread(img_path)
h, w = img_bgr.shape[:2]

r = img_bgr[:, :, 2].astype(float)
g = img_bgr[:, :, 1].astype(float)
b = img_bgr[:, :, 0].astype(float)

retina_cand = (r - b > 25) & (r - g > 5) & (r > 40)
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
cleaned = cv2.morphologyEx(retina_cand.astype(np.uint8) * 255, cv2.MORPH_CLOSE, k)
contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
largest_cnt = max(contours, key=cv2.contourArea)
(cx, cy), radius = cv2.minEnclosingCircle(largest_cnt)
cx, cy, radius = int(cx), int(cy), int(radius)

# Crop retinal circle with small margin
x1 = max(0, cx - radius)
x2 = min(w, cx + radius)
y1 = max(0, cy - radius)
y2 = min(h, cy + radius)
crop = img_bgr[y1:y2, x1:x2]

# Standardize to 512x512
std_retina = cv2.resize(crop, (512, 512), interpolation=cv2.INTER_CUBIC)

# Analyze lesions on standardized retina
import retina_analyzer
# We will use our refined lesion extractor on std_retina
res = retina_analyzer.analyze_retinal_fundus(std_retina)
print("Analysis of User's Retinal Diagram:")
print("Verified?", res.get("verified_retina"))
if res.get("verified_retina"):
    print("Grade:", res.get("grade_name"))
    print("Referable:", res.get("ref_title"))
    print("MAs detected:", res.get("mas_count"))
    print("Hemorrhages detected:", res.get("hemo_count"))
    print("Hard Exudates detected:", res.get("exudates_count"))
    print("CSME:", res.get("csme_positive"), f"(Dist: {res.get('csme_dist_dd')} DD)")
    print("Vessel Density:", res.get("vessel_density_pct"))
