import sys, urllib.request, json, base64
sys.stdout.reconfigure(encoding='utf-8')

def test_api(path, name):
    with open(path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    req = urllib.request.Request(
        'http://localhost:8080/api/analyze-retina',
        data=json.dumps({'image': b64}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    resp = urllib.request.urlopen(req, timeout=10)
    data = json.loads(resp.read().decode('utf-8'))
    print('=== ' + name + ' ===')
    print('HTTP Status:', resp.status)
    print('Verified Retina:', data.get('verified_retina'))
    if data.get('verified_retina'):
        print('Grade:', data.get('grade_name'))
        print('DR Damage Percentage:', str(data.get('dr_damage_percentage')) + '%')
        print('Urgency:', data.get('ref_title'))
        print('MAs:', data.get('mas_count'), '| Exudates:', data.get('exudates_count'), '| CSME:', data.get('csme_positive'), '(' + str(data.get('csme_dist_dd')) + ' DD)')
        print('Confidence:', data.get('verification', {}).get('confidence_pct'), '%')
    else:
        print('Error:', data.get('error'))
        print('Rejection Message:', data.get('message'))
        print('Confidence:', data.get('verification', {}).get('confidence_pct'), '%')

test_api(r'C:/Users/DELL/.gemini/antigravity/brain/83a8594b-73c9-401b-8ba6-024177eb2f1c/.user_uploaded/media_1788897068996.jpg', 'USER PORTRAIT (SUIT & GLASSES)')
test_api(r'C:/Users/DELL/.gemini/antigravity/brain/83a8594b-73c9-401b-8ba6-024177eb2f1c/.user_uploaded/media_1788899693667.webp', 'HEALTHY RETINA 1')
test_api(r'C:/Users/DELL/.gemini/antigravity/brain/83a8594b-73c9-401b-8ba6-024177eb2f1c/.user_uploaded/media_1788899711092.webp', 'HEALTHY RETINA 2')
test_api(r'C:/Users/DELL/.gemini/antigravity/brain/83a8594b-73c9-401b-8ba6-024177eb2f1c/.user_uploaded/media_1788888654346.png', 'USER RETINAL INFOGRAPHIC (SEVERE NPDR)')
