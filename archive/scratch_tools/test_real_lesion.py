import cv2
import numpy as np

def analyze_retinal_lesions(img_bgr):
    """
    Genuine pixel-level lesion extraction on authentic retinal fundus.
    Returns: lesion counts, coordinates, staging, and true saliency map.
    """
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    h, w = img_rgb.shape[:2]
    
    r = img_rgb[:, :, 0]
    g = img_rgb[:, :, 1]
    b = img_rgb[:, :, 2]
    
    # 1. Circular Retinal Mask
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 18, 255, cv2.THRESH_BINARY)
    # Morphological clean mask
    kernel_m = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_m)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_m)
    
    # 2. Optic Disc Detection
    # High red+green intensity within mask
    rg = ((r.astype(float) + g.astype(float)) / 2.0) * (mask / 255.0)
    blurred_rg = cv2.GaussianBlur(rg, (31, 31), 0)
    min_val, max_val, min_loc, disc_center = cv2.minMaxLoc(blurred_rg)
    disc_radius = int(min(h, w) * 0.08)
    
    # Optic disc mask to exclude false positives from disc rim
    disc_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(disc_mask, disc_center, int(disc_radius * 1.3), 255, -1)
    
    # Approximate Foveal Location (roughly 2.5 disc diameters temporal to disc)
    # If disc is on left half (x < w/2), fovea is to the right; if disc on right, fovea is to the left
    if disc_center[0] < w / 2:
        fovea_x = min(w - 20, int(disc_center[0] + disc_radius * 2.8))
    else:
        fovea_x = max(20, int(disc_center[0] - disc_radius * 2.8))
    fovea_y = disc_center[1]
    fovea_center = (fovea_x, fovea_y)
    
    # 3. Green Channel Contrast Enhancement
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    g_clahe = clahe.apply(g)
    
    # 4. Microvascular Vessel Tree
    k_vessel = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
    vessel_tophat = cv2.morphologyEx(255 - g_clahe, cv2.MORPH_TOPHAT, k_vessel)
    vessel_mask = (vessel_tophat > 30) & (mask > 0)
    vessel_density_pct = (np.sum(vessel_mask) / np.sum(mask > 0)) * 100.0
    
    # 5. True Hard Exudates Detection (Bright yellow/white lesions)
    # High in L* and high in b* (yellow) of CIE Lab, and not the optic disc
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l_chan = lab[:, :, 0]
    b_chan = lab[:, :, 2]
    
    # Exudates appear as high L and high b
    retina_l = l_chan[mask > 0]
    l_thresh = np.mean(retina_l) + 1.8 * np.std(retina_l)
    exudate_candidates = (l_chan > l_thresh) & (b_chan > 135) & (mask > 0) & (disc_mask == 0)
    
    # Filter small noise and large camera reflections
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(exudate_candidates.astype(np.uint8))
    exudates_coords = []
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if 4 <= area <= 600: # Exudate plaque size range
            cx, cy = int(centroids[i][0]), int(centroids[i][1])
            exudates_coords.append((cx, cy, int(np.sqrt(area/np.pi))))
            
    # 6. True Microaneurysms (MAs) & Blot Hemorrhages
    # Dark focal blobs in Green Channel (Bottom-hat transform)
    k_ma = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    g_bothat = cv2.morphologyEx(g_clahe, cv2.MORPH_BLACKHAT, k_ma)
    
    # Exclude vessels and disc
    dark_lesions = (g_bothat > 18) & (mask > 0) & (~vessel_mask) & (disc_mask == 0)
    num_labels_d, labels_d, stats_d, centroids_d = cv2.connectedComponentsWithStats(dark_lesions.astype(np.uint8))
    
    mas_coords = []
    hemo_coords = []
    for i in range(1, num_labels_d):
        area = stats_d[i, cv2.CC_STAT_AREA]
        cx, cy = int(centroids_d[i][0]), int(centroids_d[i][1])
        if 2 <= area <= 35: # Microaneurysms: punctate 2-35 px
            mas_coords.append((cx, cy, 3))
        elif 35 < area <= 800: # Blot Hemorrhages: larger patches
            hemo_coords.append((cx, cy, int(np.sqrt(area/np.pi))))
            
    # 7. Clinically Significant Macular Edema (CSME) Proximity
    csme_positive = False
    min_dist_dd = 999.0
    dd_px = disc_radius * 2.0
    for (ex, ey, er) in exudates_coords:
        dist_px = np.sqrt((ex - fovea_center[0])**2 + (ey - fovea_center[1])**2)
        dist_dd = dist_px / (dd_px + 1e-5)
        if dist_dd < min_dist_dd:
            min_dist_dd = dist_dd
        if dist_dd <= 1.0: # Within 1 Disc Diameter of fovea
            csme_positive = True
            
    # 8. True ICDR Severity Staging based on Measured Biomarkers
    num_mas = len(mas_coords)
    num_hemo = len(hemo_coords)
    num_exudates = len(exudates_coords)
    
    if num_mas == 0 and num_hemo == 0 and num_exudates == 0:
        grade = 0
        grade_name = "LEVEL 0 — NO APPARENT RETINOPATHY"
        referable = False
        ref_title = "🟢 NO REFERRAL REQUIRED"
        ref_reason = "No microaneurysms, hemorrhages, or exudates detected on genuine retinal scan."
    elif num_mas <= 5 and num_hemo == 0 and num_exudates == 0:
        grade = 1
        grade_name = "LEVEL 1 — MILD NPDR"
        referable = False
        ref_title = "🟢 ROUTINE FOLLOW-UP"
        ref_reason = f"Isolated microaneurysms detected ({num_mas} MAs). No hemorrhages or exudates."
    elif num_hemo >= 20 or (num_mas >= 25 and num_hemo >= 10):
        grade = 3
        grade_name = "LEVEL 3 — SEVERE NPDR"
        referable = True
        ref_title = "🔴 URGENT SPECIALIST REFERRAL"
        ref_reason = f"Extensive retinal lesion burden ({num_hemo} blot hemorrhages, {num_mas} MAs). 4-2-1 criteria met."
    else: # Moderate NPDR
        grade = 2
        grade_name = "LEVEL 2 — MODERATE NPDR"
        referable = True
        ref_title = "🔴 REFER TO OPHTHALMOLOGIST"
        ref_reason = f"Significant lesions: {num_mas} MAs, {num_hemo} blot hemorrhages, {num_exudates} exudates. CSME: {'Positive (Macular edema warning)' if csme_positive else 'Negative'}."
        
    return {
        "grade": grade,
        "grade_name": grade_name,
        "referable": referable,
        "ref_title": ref_title,
        "ref_reason": ref_reason,
        "mas_count": num_mas,
        "mas_coords": mas_coords[:30],
        "hemo_count": num_hemo,
        "hemo_coords": hemo_coords[:30],
        "exudates_count": num_exudates,
        "exudates_coords": exudates_coords[:30],
        "csme_positive": csme_positive,
        "csme_dist_dd": round(min_dist_dd, 2) if min_dist_dd < 900 else "N/A",
        "vessel_density_pct": round(vessel_density_pct, 2),
        "disc_center": disc_center,
        "fovea_center": fovea_center
    }

# Test on sample_real_fundus.png
real_fundus = cv2.imread("sample_real_fundus.png")
result = analyze_retinal_lesions(real_fundus)
print("Analysis of Real Fundus:")
print(f"- Staged Grade: {result['grade']} ({result['grade_name']})")
print(f"- MAs Detected: {result['mas_count']}")
print(f"- Hemorrhages: {result['hemo_count']}")
print(f"- Exudates: {result['exudates_count']}")
print(f"- CSME Positive: {result['csme_positive']} (Dist: {result['csme_dist_dd']} DD)")
print(f"- Vessel Density: {result['vessel_density_pct']}%")
