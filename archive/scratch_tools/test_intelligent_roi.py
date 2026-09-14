import cv2
import numpy as np

img_path = r'C:/Users/DELL/.gemini/antigravity/brain/83a8594b-73c9-401b-8ba6-024177eb2f1c/.user_uploaded/media_1788888654346.png'
img_bgr = cv2.imread(img_path)
h, w = img_bgr.shape[:2]

r = img_bgr[:, :, 2].astype(float)
g = img_bgr[:, :, 1].astype(float)
b = img_bgr[:, :, 0].astype(float)

# 1. Locate Retinal Region:
# Check if entire image is already a cropped retina, or if a retinal circle exists
# Retinal chromatic condition: (R - B > 25) and (R - G > 5)
retina_cand = (r - b > 25) & (r - g > 5)

total_px = h * w
cand_px = np.sum(retina_cand)
cand_ratio = cand_px / float(total_px)

print(f"Retinal chromatic pixel ratio: {cand_ratio * 100:.1f}% of image")

# Check if there is a distinct contour/circle
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
cleaned = cv2.morphologyEx(retina_cand.astype(np.uint8) * 255, cv2.MORPH_CLOSE, k)
contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if contours:
    largest_cnt = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest_cnt)
    (cx, cy), radius = cv2.minEnclosingCircle(largest_cnt)
    print(f"Largest Retinal Region: Area={area}, Center=({cx:.1f}, {cy:.1f}), Radius={radius:.1f}")
    
    # Create mask for the retinal region
    mask = np.zeros((h, w), dtype=np.uint8)
    if area > 0.10 * total_px: # Occupies at least 10% of image
        cv2.circle(mask, (int(cx), int(cy)), int(radius * 0.98), 255, -1)
    else:
        mask = cleaned
else:
    mask = np.ones((h, w), dtype=np.uint8) * 255

# Evaluate within mask
r_masked = r[mask > 0]
g_masked = g[mask > 0]
b_masked = b[mask > 0]

mean_r = np.mean(r_masked)
mean_g = np.mean(g_masked)
mean_b = np.mean(b_masked)
rb_ratio = (mean_r + 1.0) / (mean_b + 1.0)
rg_ratio = (mean_r + 1.0) / (mean_g + 1.0)

# Vessels inside mask
clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
g_enh = clahe.apply(img_bgr[:, :, 1])
k_v = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
vessel_tophat = cv2.morphologyEx(255 - g_enh, cv2.MORPH_TOPHAT, k_v)
vessel_mask = (vessel_tophat > 25) & (mask > 0)
vessel_density = float(np.sum(vessel_mask)) / float(np.sum(mask > 0))

# Optic disc inside mask
rg = ((r + g) / 2.0) * (mask / 255.0)
blurred_rg = cv2.GaussianBlur(rg, (21, 21), 0)
min_val, max_val, min_loc, disc_loc = cv2.minMaxLoc(blurred_rg)
median_rg = np.median(rg[mask > 0])
disc_contrast = max_val / (median_rg + 1.0)

print(f"\nLandmark Evaluation in Mask:")
print(f"  R/B Ratio: {rb_ratio:.2f}")
print(f"  R/G Ratio: {rg_ratio:.2f}")
print(f"  Vessel Density: {vessel_density * 100:.2f}%")
print(f"  Disc Contrast: {disc_contrast:.2f}")

is_retina = (rb_ratio > 1.25) and (rg_ratio > 1.01) and (vessel_density > 0.005) and (area > 500)
print(f"\n=> Is Authentic Retinal Image? {is_retina}")
