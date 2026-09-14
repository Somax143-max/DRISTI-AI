import cv2
import numpy as np

img_path = r'C:/Users/DELL/.gemini/antigravity/brain/83a8594b-73c9-401b-8ba6-024177eb2f1c/.user_uploaded/media_1788888654346.png'
img = cv2.imread(img_path)
h, w = img.shape[:2]

# Detect the warm retinal circle (high red-to-blue difference or saturation)
# In RGB space, retina has (R - B) significantly higher than white background or black text!
# White background: R=255, G=255, B=255 -> (R - B) ~ 0
# Black text: R=0, G=0, B=0 -> (R - B) ~ 0
# Retina: R=200, G=100, B=30 -> (R - B) ~ 170!
r = img[:, :, 2].astype(float)
g = img[:, :, 1].astype(float)
b = img[:, :, 0].astype(float)

retina_metric = (r - b) # Red-Blue difference
retina_mask = (retina_metric > 35).astype(np.uint8) * 255

# Clean with morphological opening/closing
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
retina_mask = cv2.morphologyEx(retina_mask, cv2.MORPH_CLOSE, k)
retina_mask = cv2.morphologyEx(retina_mask, cv2.MORPH_OPEN, k)

# Find largest contour (the retinal circle!)
contours, _ = cv2.findContours(retina_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print("Contours found:", len(contours))

if contours:
    largest_cnt = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest_cnt)
    print(f"Largest contour area: {area} px ({area / (w * h) * 100:.1f}% of image)")
    (cx, cy), radius = cv2.minEnclosingCircle(largest_cnt)
    print(f"Detected Retinal Circle: Center=({cx:.1f}, {cy:.1f}), Radius={radius:.1f}")
    
    # Analyze pixels ONLY INSIDE the detected retinal circle!
    mask_circle = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask_circle, (int(cx), int(cy)), int(radius * 0.95), 255, -1)
    
    circle_pixels = img[mask_circle > 0]
    mean_r_circle = np.mean(circle_pixels[:, 2])
    mean_g_circle = np.mean(circle_pixels[:, 1])
    mean_b_circle = np.mean(circle_pixels[:, 0])
    
    rb_circle = (mean_r_circle + 1) / (mean_b_circle + 1)
    rg_circle = (mean_r_circle + 1) / (mean_g_circle + 1)
    
    print(f"Inside Retinal Circle Metrics:")
    print(f"  Mean R: {mean_r_circle:.1f}, Mean G: {mean_g_circle:.1f}, Mean B: {mean_b_circle:.1f}")
    print(f"  R/B Ratio: {rb_circle:.2f} (Expected > 1.30)")
    print(f"  R/G Ratio: {rg_circle:.2f} (Expected > 1.02)")
