import cv2
import numpy as np

# Load one of our report images and inspect its dimensions
rep = cv2.imread("results/screening_report_PAT_003_MODERATE.png")
print("Report shape:", rep.shape if rep is not None else "Failed to load")

# In our report generator, the fundus canvas was plotted in the top left
# Let's crop a 400x400 patch of the fundus from the report
fundus_crop = rep[120:520, 50:450]
cv2.imwrite("sample_real_fundus.png", fundus_crop)

from test_retina_verifier import verify_retina_authenticity
is_ret, score, reasons = verify_retina_authenticity(fundus_crop)
print("Real Fundus Crop -> Is Retina?", is_ret, f"(Score: {score}/100)")
print("Reasons:", reasons)
