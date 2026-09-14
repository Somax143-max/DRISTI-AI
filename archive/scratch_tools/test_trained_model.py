import cv2, torch
import numpy as np
from train_retina_detector import RetinaEyeClassifier

model = RetinaEyeClassifier()
model.load_state_dict(torch.load('retina_eye_classifier.pth', map_location='cpu'))
model.eval()

mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)

def eval_img(path, name):
    img = cv2.imread(path)
    if img is None:
        print(name, 'could not load')
        return
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(img_rgb, (224, 224), interpolation=cv2.INTER_AREA)
    t = torch.from_numpy(resized).permute(2, 0, 1).float() / 255.0
    t = ((t - mean) / std).unsqueeze(0)
    with torch.no_grad():
        out = model(t)
        prob = torch.softmax(out, dim=1)[0]
        noneye = float(prob[0].item()) * 100
        retina = float(prob[1].item()) * 100
        v = 'RETINA' if retina > 50 else 'NON-EYE'
        print(name + ' -> Non-Eye: ' + str(round(noneye, 2)) + '%, Retina: ' + str(round(retina, 2)) + '% ==> ' + v)

eval_img(r'C:/Users/DELL/.gemini/antigravity/brain/83a8594b-73c9-401b-8ba6-024177eb2f1c/.user_uploaded/media_1788897068996.jpg', 'User Portrait (Suit & Glasses)')
eval_img(r'C:/Users/DELL/.gemini/antigravity/brain/83a8594b-73c9-401b-8ba6-024177eb2f1c/.user_uploaded/media_1788888654346.png', 'User Retinal Infographic')
eval_img('sample_real_fundus.png', 'Real Camera Fundus')
