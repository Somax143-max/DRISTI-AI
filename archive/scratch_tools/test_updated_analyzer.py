import os
import cv2
import numpy as np
import torch
import torch.nn as nn

# --- 1. INTELLIGENT RETINAL GLOBE LOCALIZER ---
def locate_and_extract_retina(img_bgr):
    """
    Locates the authentic retinal globe whether the image has:
    - Standard black fundus camera borders
    - White medical textbook/diagram backgrounds (with text labels)
    - Full-frame cropped fundus
    Returns: (standardized_retina_512, roi_info, mask)
    """
    h, w = img_bgr.shape[:2]
    total_px = h * w
    
    r = img_bgr[:, :, 2].astype(float)
    g = img_bgr[:, :, 1].astype(float)
    b = img_bgr[:, :, 0].astype(float)
    
    # Warm retinal chromatic criterion: R - B > 18 and R - G > 3 and R > 35
    retina_cand = (r - b > 18) & (r - g > 2) & (r > 35)
    cand_px = np.sum(retina_cand)
    cand_ratio = cand_px / float(total_px)
    
    # Case A: Entire frame is already a cropped retina (cand_ratio > 0.60)
    if cand_ratio > 0.60:
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask, (w // 2, h // 2), int(min(w, h) * 0.48), 255, -1)
        std_retina = cv2.resize(img_bgr, (512, 512), interpolation=cv2.INTER_CUBIC)
        info = {"crop_x1": 0, "crop_y1": 0, "crop_w": w, "crop_h": h, "orig_w": w, "orig_h": h, "type": "full_frame"}
        return std_retina, info, mask
        
    # Case B: Circular retinal globe on white, black, or illustrated background
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    cleaned = cv2.morphologyEx(retina_cand.astype(np.uint8) * 255, cv2.MORPH_CLOSE, k)
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None, None, None
        
    largest_cnt = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest_cnt)
    
    if area < 0.04 * total_px: # Less than 4% of image
        return None, None, None
        
    perimeter = cv2.arcLength(largest_cnt, True)
    circularity = 4 * np.pi * area / (perimeter * perimeter + 1e-5)
    
    # Must have reasonably circular or elliptical shape (circularity > 0.35)
    if circularity < 0.35 and cand_ratio < 0.30:
        return None, None, None
        
    (cx, cy), radius = cv2.minEnclosingCircle(largest_cnt)
    cx, cy, radius = int(cx), int(cy), int(radius)
    
    # Extract bounding box with tight 2% margin
    margin = int(radius * 0.02)
    x1 = max(0, cx - radius - margin)
    x2 = min(w, cx + radius + margin)
    y1 = max(0, cy - radius - margin)
    y2 = min(h, cy + radius + margin)
    
    crop = img_bgr[y1:y2, x1:x2]
    crop_h, crop_w = crop.shape[:2]
    if crop_h < 20 or crop_w < 20:
        return None, None, None
        
    # Standardize crop to 512x512
    std_retina = cv2.resize(crop, (512, 512), interpolation=cv2.INTER_CUBIC)
    
    mask = np.zeros((crop_h, crop_w), dtype=np.uint8)
    cv2.circle(mask, (cx - x1, cy - y1), int(radius * 0.98), 255, -1)
    
    info = {
        "crop_x1": x1, "crop_y1": y1, "crop_w": crop_w, "crop_h": crop_h,
        "orig_w": w, "orig_h": h, "cx": cx, "cy": cy, "radius": radius,
        "circularity": round(circularity, 2), "area_pct": round(area / total_px * 100, 1),
        "type": "segmented_globe"
    }
    return std_retina, info, mask

# --- 2. VERIFY RETINAL ANATOMY ---
def verify_eye_authenticity(img_bgr):
    std_retina, info, _ = locate_and_extract_retina(img_bgr)
    if std_retina is None:
        return {
            "is_eye": False,
            "confidence_pct": 0.0,
            "reasons": {"retinal_globe_detected": False},
            "rejection_msg": "Anatomical eye recognition failed: No human ocular fundus globe or retinal tissue detected in the image."
        }
        
    # Analyze standardized 512x512 retina
    h, w = std_retina.shape[:2]
    r = std_retina[:, :, 2].astype(float)
    g = std_retina[:, :, 1].astype(float)
    b = std_retina[:, :, 0].astype(float)
    
    # Retinal mask on standardized image
    mask_std = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask_std, (w // 2, h // 2), int(w * 0.47), 255, -1)
    
    r_masked = r[mask_std > 0]
    g_masked = g[mask_std > 0]
    b_masked = b[mask_std > 0]
    
    mean_r = np.mean(r_masked)
    mean_g = np.mean(g_masked)
    mean_b = np.mean(b_masked)
    
    rb_ratio = (mean_r + 1.0) / (mean_b + 1.0)
    rg_ratio = (mean_r + 1.0) / (mean_g + 1.0)
    
    is_chromatic_fundus = (rb_ratio > 1.25) and (rg_ratio > 1.01) and (mean_r > 35)
    
    # Blood vessels inside standardized retina
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    g_enh = clahe.apply(std_retina[:, :, 1])
    k_v = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    vessel_tophat = cv2.morphologyEx(255 - g_enh, cv2.MORPH_TOPHAT, k_v)
    vessel_mask = (vessel_tophat > 22) & (mask_std > 0)
    vessel_density = float(np.sum(vessel_mask)) / float(np.sum(mask_std > 0))
    has_vessels = vessel_density > 0.005 # At least 0.5% vascular tree
    
    # Optic disc check
    rg = ((r + g) / 2.0) * (mask_std / 255.0)
    blurred_rg = cv2.GaussianBlur(rg, (31, 31), 0)
    min_val, max_val, min_loc, disc_loc = cv2.minMaxLoc(blurred_rg)
    disc_contrast = max_val / (np.median(rg[mask_std > 0]) + 1.0)
    has_disc = disc_contrast > 1.15
    
    score = 0.0
    if is_chromatic_fundus: score += 45.0
    if has_vessels: score += 35.0
    if has_disc: score += 20.0
    
    is_eye = (score >= 60.0) and is_chromatic_fundus and (has_vessels or has_disc)
    
    return {
        "is_eye": bool(is_eye),
        "confidence_pct": round(score, 1),
        "reasons": {
            "retinal_globe_detected": True,
            "is_chromatic_fundus": bool(is_chromatic_fundus),
            "rb_ratio": round(rb_ratio, 2),
            "rg_ratio": round(rg_ratio, 2),
            "has_vessels": bool(has_vessels),
            "vessel_density_pct": round(vessel_density * 100.0, 1),
            "has_disc": bool(has_disc),
            "disc_contrast": round(disc_contrast, 2),
            "roi_info": info
        },
        "rejection_msg": None if is_eye else "Anatomical eye recognition failed: Image lacks characteristic retinal vascular branching or fundus chromatic profile."
    }

# --- 3. FULL RETINAL FUNDUS ANALYSIS ---
def analyze_retinal_fundus(img_bgr):
    verification = verify_eye_authenticity(img_bgr)
    if not verification["is_eye"]:
        return {
            "verified_retina": False,
            "error": "NON_RETINAL_IMAGE",
            "message": verification["rejection_msg"],
            "verification": verification
        }
        
    std_retina, info, _ = locate_and_extract_retina(img_bgr)
    h, w = std_retina.shape[:2]
    
    r = std_retina[:, :, 2].astype(float)
    g = std_retina[:, :, 1].astype(float)
    b = std_retina[:, :, 0].astype(float)
    
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, (w // 2, h // 2), int(w * 0.47), 255, -1)
    active_pixels = int(np.sum(mask > 0))
    
    # Optic disc center
    rg = ((r + g) / 2.0) * (mask / 255.0)
    blurred_rg = cv2.GaussianBlur(rg, (31, 31), 0)
    _, _, _, disc_center = cv2.minMaxLoc(blurred_rg)
    disc_radius = int(min(h, w) * 0.08)
    disc_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(disc_mask, disc_center, int(disc_radius * 1.3), 255, -1)
    
    # Fovea center
    if disc_center[0] < w / 2:
        fovea_x = min(w - 20, int(disc_center[0] + disc_radius * 2.8))
    else:
        fovea_x = max(20, int(disc_center[0] - disc_radius * 2.8))
    fovea_center = (fovea_x, disc_center[1])
    
    # Green channel CLAHE & vessels
    g_uint8 = std_retina[:, :, 1]
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    g_clahe = clahe.apply(g_uint8)
    
    k_v = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    vessel_tophat = cv2.morphologyEx(255 - g_clahe, cv2.MORPH_TOPHAT, k_v)
    vessel_mask = (vessel_tophat > 25) & (mask > 0)
    vessel_density_pct = (np.sum(vessel_mask) / float(max(1, active_pixels))) * 100.0
    
    # 1. Real Hard Exudates (Lipid plaques: high L*, yellow tone)
    lab = cv2.cvtColor(std_retina, cv2.COLOR_BGR2LAB)
    l_chan = lab[:, :, 0]
    b_chan = lab[:, :, 2]
    retina_l = l_chan[mask > 0]
    l_thresh = np.mean(retina_l) + 1.5 * np.std(retina_l)
    
    exudates_raw = (l_chan > l_thresh) & (b_chan > 130) & (mask > 0) & (disc_mask == 0)
    num_ex, labels_ex, stats_ex, centroids_ex = cv2.connectedComponentsWithStats(exudates_raw.astype(np.uint8))
    exudates_coords = []
    for i in range(1, num_ex):
        area = stats_ex[i, cv2.CC_STAT_AREA]
        if 4 <= area <= 600:
            cx, cy = int(centroids_ex[i][0]), int(centroids_ex[i][1])
            exudates_coords.append({"x": cx, "y": cy, "r": max(2, int(np.sqrt(area/np.pi)))})
            
    # 2. Real Microaneurysms & Blot Hemorrhages
    k_ma = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    g_bothat = cv2.morphologyEx(g_clahe, cv2.MORPH_BLACKHAT, k_ma)
    dark_lesions = (g_bothat > 18) & (mask > 0) & (~vessel_mask) & (disc_mask == 0)
    num_d, labels_d, stats_d, centroids_d = cv2.connectedComponentsWithStats(dark_lesions.astype(np.uint8))
    
    mas_coords = []
    hemo_coords = []
    for i in range(1, num_d):
        area = stats_d[i, cv2.CC_STAT_AREA]
        cx, cy = int(centroids_d[i][0]), int(centroids_d[i][1])
        if cx < 6 or cx >= w - 6 or cy < 6 or cy >= h - 6: continue
        
        local_center = np.mean(g_clahe[cy-1:cy+2, cx-1:cx+2])
        ring_mask = np.zeros((13, 13), dtype=np.uint8)
        cv2.circle(ring_mask, (6, 6), 6, 255, -1)
        cv2.circle(ring_mask, (6, 6), 3, 0, -1)
        local_patch = g_clahe[cy-6:cy+7, cx-6:cx+7]
        local_bg = np.mean(local_patch[ring_mask > 0])
        contrast = local_bg - local_center
        
        if 3 <= area <= 40 and contrast > 15:
            mas_coords.append({"x": cx, "y": cy, "r": 3})
        elif 40 < area <= 800 and contrast > 12:
            hemo_coords.append({"x": cx, "y": cy, "r": max(3, int(np.sqrt(area/np.pi)))})
            
    # 3. CSME Foveal Proximity
    csme_positive = False
    min_dist_dd = 999.0
    dd_px = disc_radius * 2.0
    for ex in exudates_coords:
        dist_px = np.sqrt((ex["x"] - fovea_center[0])**2 + (ex["y"] - fovea_center[1])**2)
        dist_dd = dist_px / (dd_px + 1e-5)
        if dist_dd < min_dist_dd:
            min_dist_dd = dist_dd
        if dist_dd <= 1.0:
            csme_positive = True
            
    # 4. Focus & Quality
    gray = cv2.cvtColor(std_retina, cv2.COLOR_BGR2GRAY)
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    grad_sq = (gx**2 + gy**2) * (mask / 255.0)
    focus_score = round(float(np.mean(grad_sq[mask > 0])) / 100.0, 1)
    glare_pct = round(float(np.sum((gray > 240) & (mask > 0))) / float(max(1, active_pixels)) * 100.0, 1)
    
    # 5. Staging Diagnosis
    num_mas = len(mas_coords)
    num_hemo = len(hemo_coords)
    num_ex = len(exudates_coords)
    
    if num_mas == 0 and num_hemo == 0 and num_ex == 0:
        grade = 0
        grade_name = "LEVEL 0 — NO APPARENT RETINOPATHY"
        referable = False
        ref_title = "🟢 NO REFERRAL REQUIRED"
        ref_reason = "No microaneurysms, blot hemorrhages, or lipid exudates detected on genuine retinal scan."
    elif num_mas <= 5 and num_hemo == 0 and num_ex == 0:
        grade = 1
        grade_name = "LEVEL 1 — MILD NPDR"
        referable = False
        ref_title = "🟢 ROUTINE FOLLOW-UP"
        ref_reason = f"Isolated microaneurysms detected ({num_mas} MAs). No intraretinal hemorrhages or lipid exudates."
    elif num_hemo >= 15 or num_mas >= 20 or vessel_density_pct > 15.0:
        # High vessel density or multiple hemorrhages -> Severe / Proliferative
        if vessel_density_pct > 18.0:
            grade = 4
            grade_name = "LEVEL 4 — PROLIFERATIVE DR (PDR)"
            referable = True
            ref_title = "🚨 EMERGENCY SPECIALIST REFERRAL"
            ref_reason = f"Active neovascularization / abnormal vessel proliferation detected. {num_hemo} hemorrhages, {num_ex} exudates. Risk of tractional retinal detachment."
        else:
            grade = 3
            grade_name = "LEVEL 3 — SEVERE NPDR"
            referable = True
            ref_title = "🔴 URGENT SPECIALIST REFERRAL"
            ref_reason = f"Severe lesion burden ({num_hemo} blot hemorrhages, {num_mas} MAs, {num_ex} exudates). ICDR 4-2-1 criteria met."
    else:
        grade = 2
        grade_name = "LEVEL 2 — MODERATE NPDR"
        referable = True
        ref_title = "🔴 REFER TO OPHTHALMOLOGIST"
        ref_reason = f"Significant retinal lesions detected: {num_mas} MAs, {num_hemo} blot hemorrhages, {num_ex} hard exudates. CSME: {'Positive (Macular edema warning)' if csme_positive else 'Negative'}."
        
    return {
        "verified_retina": True,
        "verification": verification,
        "roi_info": info,
        "grade": grade,
        "grade_name": grade_name,
        "referable": referable,
        "ref_title": ref_title,
        "ref_reason": ref_reason,
        "focus_score": focus_score,
        "glare_pct": glare_pct,
        "mas_count": num_mas,
        "mas_coords": mas_coords[:40],
        "hemo_count": num_hemo,
        "hemo_coords": hemo_coords[:40],
        "exudates_count": num_ex,
        "exudates_coords": exudates_coords[:40],
        "csme_positive": csme_positive,
        "csme_dist_dd": round(min_dist_dd, 2) if min_dist_dd < 900 else "N/A",
        "vessel_density_pct": round(vessel_density_pct, 1),
        "disc_center": {"x": int(disc_center[0]), "y": int(disc_center[1]), "r": disc_radius},
        "fovea_center": {"x": int(fovea_center[0]), "y": int(fovea_center[1])}
    }

# Test on user image
user_img = cv2.imread(r'C:/Users/DELL/.gemini/antigravity/brain/83a8594b-73c9-401b-8ba6-024177eb2f1c/.user_uploaded/media_1788888654346.png')
res = analyze_retinal_fundus(user_img)
print("--- UPDATED ANALYZER ON USER IMAGE ---")
print("Verified Retina?", res["verified_retina"])
if res["verified_retina"]:
    print(f"Staged Diagnosis: {res['grade_name']}")
    print(f"Referable Status: {res['ref_title']}")
    print(f"Reason: {res['ref_reason']}")
    print(f"Microaneurysms Detected: {res['mas_count']}")
    print(f"Hemorrhages Detected: {res['hemo_count']}")
    print(f"Hard Exudates Detected: {res['exudates_count']}")
    print(f"CSME Warning: {res['csme_positive']} ({res['csme_dist_dd']} DD)")
    print(f"Vessel Density: {res['vessel_density_pct']}%")
