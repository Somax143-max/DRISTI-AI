import cv2
import numpy as np

def verify_retina_authenticity(img_bgr):
    """
    Rigorously verifies if an image is an authentic retinal fundus photograph.
    Returns: (is_retina, confidence_score, reasons_dict)
    """
    h, w = img_bgr.shape[:2]
    total_pixels = h * w
    
    # 1. Color Space Diagnostics
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    r = img_rgb[:, :, 0].astype(float)
    g = img_rgb[:, :, 1].astype(float)
    b = img_rgb[:, :, 2].astype(float)
    
    mean_r = np.mean(r)
    mean_g = np.mean(g)
    mean_b = np.mean(b)
    
    # In authentic human fundus, red dominates over blue due to RPE and choroidal hemoglobin
    # Ratio R/B should typically be > 1.4 in active retinal area
    rb_ratio = (mean_r + 1.0) / (mean_b + 1.0)
    rg_ratio = (mean_r + 1.0) / (mean_g + 1.0)
    
    # 2. Circular Aperture / Mask Check
    # Real fundus photos have dark borders/corners (FOV aperture)
    corner_size = int(min(h, w) * 0.08)
    corners = [
        img_rgb[:corner_size, :corner_size],
        img_rgb[:corner_size, -corner_size:],
        img_rgb[-corner_size:, :corner_size],
        img_rgb[-corner_size:, -corner_size:]
    ]
    corner_means = [np.mean(c) for c in corners]
    avg_corner_brightness = np.mean(corner_means)
    
    # Active center brightness
    center_box = img_rgb[int(h*0.25):int(h*0.75), int(w*0.25):int(w*0.75)]
    center_brightness = np.mean(center_box)
    
    has_aperture_contrast = (center_brightness > 30) and (avg_corner_brightness < center_brightness * 0.75)
    
    # 3. Retinal Blood Vessel Continuity in Green Channel
    # Green channel inverted gives high vessel contrast
    g_ch = img_rgb[:, :, 1]
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    g_enhanced = clahe.apply(g_ch)
    
    # Morphological top-hat to detect linear vessel segments
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    tophat = cv2.morphologyEx(255 - g_enhanced, cv2.MORPH_TOPHAT, kernel)
    vessel_candidates = tophat > 25
    vessel_density = np.sum(vessel_candidates) / float(total_pixels)
    
    # 4. Optic Disc Candidate Search
    # Brightest focal region in (R+G)
    rg_sum = (r + g) / 2.0
    blurred_rg = cv2.GaussianBlur(rg_sum, (21, 21), 0)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(blurred_rg)
    disc_contrast = max_val / (np.median(rg_sum) + 1.0)
    
    # Decision Logic
    is_chromatic_fundus = (rb_ratio > 1.35) and (rg_ratio > 1.05) and (mean_r > 35)
    has_vessels = (0.008 <= vessel_density <= 0.25)
    has_disc = (disc_contrast > 1.25)
    
    reasons = {
        "rb_ratio": round(rb_ratio, 2),
        "rg_ratio": round(rg_ratio, 2),
        "mean_r": round(mean_r, 1),
        "mean_b": round(mean_b, 1),
        "corner_brightness": round(avg_corner_brightness, 1),
        "center_brightness": round(center_brightness, 1),
        "has_aperture_contrast": bool(has_aperture_contrast),
        "vessel_density_pct": round(vessel_density * 100, 2),
        "has_vessels": bool(has_vessels),
        "disc_contrast": round(disc_contrast, 2),
        "has_disc": bool(has_disc),
        "is_chromatic_fundus": bool(is_chromatic_fundus)
    }
    
    # Score out of 100
    score = 0
    if is_chromatic_fundus: score += 40
    if has_vessels: score += 25
    if has_disc: score += 20
    if has_aperture_contrast: score += 15
    
    is_retina = (score >= 65) and is_chromatic_fundus and (has_vessels or has_disc)
    
    return is_retina, score, reasons

# Test on synthetic non-retina images
# 1. Random noise
noise_img = np.random.randint(0, 256, (512, 512, 3), dtype=np.uint8)
is_ret, score, r = verify_retina_authenticity(noise_img)
print("1. Random Noise Image -> Is Retina?", is_ret, f"(Score: {score}/100)")

# 2. Blue sky / landscape
landscape_img = np.zeros((512, 512, 3), dtype=np.uint8)
landscape_img[:, :, 0] = 200 # Blue
landscape_img[:, :, 1] = 150 # Green
landscape_img[:, :, 2] = 50  # Red
is_ret, score, r = verify_retina_authenticity(landscape_img)
print("2. Blue/Landscape Image -> Is Retina?", is_ret, f"(Score: {score}/100)")

# 3. Document / Text
doc_img = np.ones((512, 512, 3), dtype=np.uint8) * 240
is_ret, score, r = verify_retina_authenticity(doc_img)
print("3. White Document Image -> Is Retina?", is_ret, f"(Score: {score}/100)")

# 4. Portrait/Face simulation (skin tones, but uniform, no circular aperture or retinal vessels)
skin_img = np.zeros((512, 512, 3), dtype=np.uint8)
skin_img[:, :, 0] = 160 # B
skin_img[:, :, 1] = 190 # G
skin_img[:, :, 2] = 230 # R
is_ret, score, r = verify_retina_authenticity(skin_img)
print("4. Skin Portrait Image -> Is Retina?", is_ret, f"(Score: {score}/100)")
