import cv2
import numpy as np

def locate_retinal_globe(img_bgr):
    h, w = img_bgr.shape[:2]
    total_px = h * w
    r = img_bgr[:, :, 2].astype(float)
    g = img_bgr[:, :, 1].astype(float)
    b = img_bgr[:, :, 0].astype(float)
    
    # Retinal chromatic condition: warm melanin/hemoglobin tones
    retina_cand = (r - b > 20) & (r - g > 3) & (r > 35)
    cand_px = np.sum(retina_cand)
    cand_ratio = cand_px / float(total_px)
    
    if cand_ratio < 0.05:
        return None, None, {"error": "No retinal chromatic tissue detected"}
        
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    cleaned = cv2.morphologyEx(retina_cand.astype(np.uint8) * 255, cv2.MORPH_CLOSE, k)
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, None, {"error": "No contiguous retinal contour"}
        
    largest_cnt = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest_cnt)
    
    if area < 0.05 * total_px:
        return None, None, {"error": "Retinal candidate area too small"}
        
    (cx, cy), radius = cv2.minEnclosingCircle(largest_cnt)
    cx, cy, radius = int(cx), int(cy), int(radius)
    
    # Retinal bounding box with a 4% margin
    margin = int(radius * 0.04)
    x1 = max(0, cx - radius - margin)
    x2 = min(w, cx + radius + margin)
    y1 = max(0, cy - radius - margin)
    y2 = min(h, cy + radius + margin)
    
    crop = img_bgr[y1:y2, x1:x2]
    
    # Internal circular mask within crop
    crop_h, crop_w = crop.shape[:2]
    mask = np.zeros((crop_h, crop_w), dtype=np.uint8)
    cv2.circle(mask, (cx - x1, cy - y1), int(radius * 0.98), 255, -1)
    
    info = {
        "x1": x1, "y1": y1, "x2": x2, "y2": y2,
        "cx": cx, "cy": cy, "radius": radius,
        "area_pct": round(area / total_px * 100, 1)
    }
    return crop, mask, info

# Test on user's image
user_img = cv2.imread(r'C:/Users/DELL/.gemini/antigravity/brain/83a8594b-73c9-401b-8ba6-024177eb2f1c/.user_uploaded/media_1788888654346.png')
crop, mask, info = locate_retinal_globe(user_img)
print("User Image Retinal Globe Detection:")
print("Info:", info)
print("Crop shape:", crop.shape if crop is not None else None)

# Test on non-eye images
for name, non_img in [
    ("Random Noise", np.random.randint(0, 256, (300, 300, 3), dtype=np.uint8)),
    ("White Document", np.ones((300, 300, 3), dtype=np.uint8)*245),
    ("Landscape", np.array([[[200, 150, 50]]*300]*300, dtype=np.uint8))
]:
    c, m, inf = locate_retinal_globe(non_img)
    print(f"{name} -> Globe Found?", c is not None, f"({inf.get('error')})")
