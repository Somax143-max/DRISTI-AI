import sys
sys.stdout.reconfigure(encoding='utf-8')
import urllib.request
import json
import base64

img_path = r'C:/Users/DELL/.gemini/antigravity/brain/83a8594b-73c9-401b-8ba6-024177eb2f1c/.user_uploaded/media_1788888654346.png'
with open(img_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

req = urllib.request.Request(
    'http://localhost:8080/api/analyze-retina',
    data=json.dumps({'image': b64}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

resp = urllib.request.urlopen(req, timeout=10)
data = json.loads(resp.read().decode('utf-8'))

print("=== SERVER API LIVE TEST ON USER'S UPLOADED IMAGE ===")
print("Status Code:", resp.status)
print("Verified Retina?", data.get('verified_retina'))
print("Grade:", data.get('grade_name'))
print("Referral Urgency:", data.get('ref_title'))
print("Reason:", data.get('ref_reason'))
print("Microaneurysms Detected:", data.get('mas_count'))
print("Hard Exudates Detected:", data.get('exudates_count'))
print("Hemorrhages Detected:", data.get('hemo_count'))
print("CSME Positive:", data.get('csme_positive'), f"({data.get('csme_dist_dd')} DD)")
print("Vessel Density:", data.get('vessel_density_pct'), "%")
