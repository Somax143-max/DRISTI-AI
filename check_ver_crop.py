import cv2
import retina_analyzer

img = cv2.imread("user_retina_isolated.png")
ver = retina_analyzer.verify_eye_authenticity(img)
print("Score:", ver["confidence_pct"])
print("Reasons:", ver["reasons"])
print("Rejection msg:", ver.get("rejection_msg"))
