import cv2
import numpy as np
import torch
import torch.nn as nn
from PIL import Image

print("PyTorch and OpenCV loaded successfully.")
print("CUDA Available:", torch.cuda.is_available())
print("Device:", "cuda" if torch.cuda.is_available() else "cpu")
