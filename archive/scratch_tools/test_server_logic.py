import json
import base64
import urllib.request
import cv2
import numpy as np
import retina_analyzer

# Test direct analysis call
sample = cv2.imread("sample_real_fundus.png")
res = retina_analyzer.analyze_retinal_fundus(sample)
print("Direct Analysis Test Result:")
print("- Verified Retina?", res["verified_retina"])
print("- Grade:", res.get("grade_name"))
print("- MAs Count:", res.get("mas_count"))
print("- Exudates Count:", res.get("exudates_count"))

# Test with a non-retinal image (e.g. gray image with text)
non_eye = np.ones((400, 400, 3), dtype=np.uint8) * 200
cv2.putText(non_eye, "INVOICE #4910", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
res_non = retina_analyzer.analyze_retinal_fundus(non_eye)
print("\nNon-Eye Document Test Result:")
print("- Verified Retina?", res_non["verified_retina"])
print("- Error Code:", res_non.get("error"))
print("- Message:", res_non.get("message"))
