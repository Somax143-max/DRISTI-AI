import cv2
import numpy as np

# Load real fundus crop
img = cv2.imread("sample_real_fundus.png")
h, w = img.shape[:2]
g = img[:, :, 1]

# Retinal mask
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, mask = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)

# Green channel CLAHE
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
g_enh = clahe.apply(g)

# Vessel mask to exclude vessel branches
k_v = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
vessel_tophat = cv2.morphologyEx(255 - g_enh, cv2.MORPH_TOPHAT, k_v)
vessel_mask = vessel_tophat > 25

# Optic disc mask
rg = ((img[:,:,2].astype(float) + img[:,:,1].astype(float))/2.0) * (mask/255.0)
blurred_rg = cv2.GaussianBlur(rg, (31, 31), 0)
_, _, _, disc_center = cv2.minMaxLoc(blurred_rg)
disc_radius = int(min(h, w) * 0.08)
disc_mask = np.zeros((h, w), dtype=np.uint8)
cv2.circle(disc_mask, disc_center, int(disc_radius * 1.3), 255, -1)

# Black-hat for dark focal spots
k_ma = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
bothat = cv2.morphologyEx(g_enh, cv2.MORPH_BLACKHAT, k_ma)
candidates = (bothat > 20) & (mask > 0) & (~vessel_mask) & (disc_mask == 0)

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(candidates.astype(np.uint8))
true_mas = []
true_hemos = []

for i in range(1, num_labels):
    area = stats[i, cv2.CC_STAT_AREA]
    cx, cy = int(centroids[i][0]), int(centroids[i][1])
    
    # Check boundaries
    if cx < 6 or cx >= w - 6 or cy < 6 or cy >= h - 6:
        continue
        
    # Local background contrast in green channel
    local_center = np.mean(g_enh[cy-1:cy+2, cx-1:cx+2])
    # Ring from 3 to 6 px
    ring_mask = np.zeros((13, 13), dtype=np.uint8)
    cv2.circle(ring_mask, (6, 6), 6, 255, -1)
    cv2.circle(ring_mask, (6, 6), 3, 0, -1)
    local_patch = g_enh[cy-6:cy+7, cx-6:cx+7]
    local_bg = np.mean(local_patch[ring_mask > 0])
    
    contrast = local_bg - local_center
    
    if 3 <= area <= 40 and contrast > 18:
        true_mas.append((cx, cy))
    elif 40 < area <= 800 and contrast > 15:
        true_hemos.append((cx, cy))

print(f"Refined Real Lesion Counts on Sample Fundus:")
print(f"- Real Microaneurysms (MAs): {len(true_mas)}")
print(f"- Real Blot Hemorrhages: {len(true_hemos)}")
