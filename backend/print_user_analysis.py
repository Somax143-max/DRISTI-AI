import sys
sys.stdout.reconfigure(encoding='utf-8')
import cv2
import test_updated_analyzer

img = cv2.imread(r'C:/Users/DELL/.gemini/antigravity/brain/83a8594b-73c9-401b-8ba6-024177eb2f1c/.user_uploaded/media_1788888654346.png')
res = test_updated_analyzer.analyze_retinal_fundus(img)
print("=== ANALYSIS OF USER'S DIABETIC RETINOPATHY IMAGE ===")
print("Verified Retina?", res['verified_retina'])
print("Grade:", res['grade_name'])
print("Referral Urgency:", res['ref_title'])
print("Clinical Rationale:", res['ref_reason'])
print("Microaneurysms Detected:", res['mas_count'])
print("Blot Hemorrhages Detected:", res['hemo_count'])
print("Hard Exudates Detected:", res['exudates_count'])
print("CSME Positive:", res['csme_positive'], f"({res['csme_dist_dd']} DD)")
print("Vessel Density:", res['vessel_density_pct'], "%")
