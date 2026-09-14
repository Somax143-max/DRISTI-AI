import cv2
import numpy as np
import retina_analyzer

# 1. Real fundus
real_f = cv2.imread('sample_real_fundus.png')
res_real = retina_analyzer.analyze_retinal_fundus(real_f)
print("Real Fundus -> Verified?", res_real['verified_retina'])
if res_real['verified_retina']:
    print(f"  Grade: {res_real['grade']} ({res_real['grade_name']})")
    print(f"  PyTorch Confidence: {res_real['verification']['reasons']['pytorch_confidence']}%")
    print(f"  MAs: {res_real['mas_count']}, Hemo: {res_real['hemo_count']}, Exudates: {res_real['exudates_count']}")

# 2. Non-eye: random noise
noise = np.random.randint(0, 256, (512, 512, 3), dtype=np.uint8)
res_noise = retina_analyzer.analyze_retinal_fundus(noise)
print("\nNoise Image -> Verified?", res_noise['verified_retina'])
print("  Error:", res_noise.get('error'))
print("  Message:", res_noise.get('message'))

# 3. Non-eye: document
doc = np.ones((512, 512, 3), dtype=np.uint8) * 245
res_doc = retina_analyzer.analyze_retinal_fundus(doc)
print("\nWhite Document -> Verified?", res_doc['verified_retina'])
print("  Error:", res_doc.get('error'))
