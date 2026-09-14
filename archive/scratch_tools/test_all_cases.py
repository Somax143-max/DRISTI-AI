import cv2
import numpy as np

def check_image(img_bgr, label):
    h, w = img_bgr.shape[:2]
    total_px = h * w
    r = img_bgr[:, :, 2].astype(float)
    g = img_bgr[:, :, 1].astype(float)
    b = img_bgr[:, :, 0].astype(float)
    
    # 1. Retinal chromatic test
    retina_cand = (r - b > 25) & (r - g > 5) & (r > 40)
    cand_ratio = np.sum(retina_cand) / float(total_px)
    
    if cand_ratio < 0.08: # If less than 8% of the image has retinal warm color
        print(f"[{label}] -> REJECTED (No retinal chromatic tissue, ratio={cand_ratio*100:.1f}%)")
        return False
        
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    cleaned = cv2.morphologyEx(retina_cand.astype(np.uint8) * 255, cv2.MORPH_CLOSE, k)
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print(f"[{label}] -> REJECTED (No contiguous retinal region)")
        return False
        
    largest_cnt = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest_cnt)
    if area < 0.08 * total_px:
        print(f"[{label}] -> REJECTED (Retinal area too small, {area/total_px*100:.1f}%)")
        return False
        
    (cx, cy), radius = cv2.minEnclosingCircle(largest_cnt)
    # Check circularity of the contour
    perimeter = cv2.arcLength(largest_cnt, True)
    if perimeter > 0:
        circularity = 4 * np.pi * (area / (perimeter * perimeter))
    else:
        circularity = 0
        
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, (int(cx), int(cy)), int(radius * 0.95), 255, -1)
    
    r_masked = r[mask > 0]
    g_masked = g[mask > 0]
    b_masked = b[mask > 0]
    
    rb_ratio = (np.mean(r_masked) + 1.0) / (np.mean(b_masked) + 1.0)
    rg_ratio = (np.mean(r_masked) + 1.0) / (np.mean(g_masked) + 1.0)
    
    # Blood vessels inside the mask
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    g_enh = clahe.apply(img_bgr[:, :, 1])
    k_v = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    vessel_tophat = cv2.morphologyEx(255 - g_enh, cv2.MORPH_TOPHAT, k_v)
    vessel_mask = (vessel_tophat > 22) & (mask > 0)
    vessel_density = float(np.sum(vessel_mask)) / float(np.sum(mask > 0))
    
    is_ret = (rb_ratio > 1.25) and (rg_ratio > 1.01) and (vessel_density > 0.005)
    print(f"[{label}] -> {'VERIFIED AS RETINA' if is_ret else 'REJECTED'} (RB={rb_ratio:.2f}, RG={rg_ratio:.2f}, Vessels={vessel_density*100:.1f}%)")
    return is_ret

# Test on user's image
user_img = cv2.imread(r'C:/Users/DELL/.gemini/antigravity/brain/83a8594b-73c9-401b-8ba6-024177eb2f1c/.user_uploaded/media_1788888654346.png')
check_image(user_img, "User's DR Diagram")

# Test on non-eye images
check_image(np.random.randint(0, 256, (300, 300, 3), dtype=np.uint8), "Random Noise")
check_image(np.ones((300, 300, 3), dtype=np.uint8)*240, "White Document")
check_image(np.array([[[200, 150, 50]]*300]*300, dtype=np.uint8), "Landscape")
check_image(np.array([[[160, 190, 230]]*300]*300, dtype=np.uint8), "Skin Photo")
