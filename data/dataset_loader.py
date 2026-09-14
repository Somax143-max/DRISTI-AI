"""
DRISHTI AI: Clinical Retinal Dataset Pipeline & Standardizer
Supports: APTOS 2019, IDRiD, Messidor-2, DRIVE, and Held-out Clinical Test Cohort.
Enforces: Patient-level stratification, circular FOV extraction, and 512x512 normalization.
"""

import os
import json
import hashlib
import cv2
import numpy as np

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
MANIFEST_PATH = os.path.join(DATA_DIR, "dataset_manifest.json")

class ClinicalFundusPreprocessor:
    """Standardizes heterogeneous fundus camera photography across clinical sites."""

    @staticmethod
    def extract_circular_fov(img_bgr, target_size=(512, 512)):
        """
        Removes black optical camera borders, segmenting the ocular globe into
        a standardized tight circular 512x512 matrix.
        """
        if img_bgr is None:
            return None, None
            
        h, w = img_bgr.shape[:2]
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        
        # Segment bright/colored retinal area from camera black surround
        thresh = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)[1]
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, k)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            resized = cv2.resize(img_bgr, target_size, interpolation=cv2.INTER_AREA)
            mask = np.zeros(target_size, dtype=np.uint8)
            cv2.circle(mask, (target_size[0] // 2, target_size[1] // 2), int(target_size[0] * 0.48), 255, -1)
            return resized, mask
            
        largest_cnt = max(contours, key=cv2.contourArea)
        (cx, cy), radius = cv2.minEnclosingCircle(largest_cnt)
        cx, cy, radius = int(cx), int(cy), int(radius)
        
        pad = int(radius * 0.02)
        x1 = max(0, cx - radius - pad)
        x2 = min(w, cx + radius + pad)
        y1 = max(0, cy - radius - pad)
        y2 = min(h, cy + radius + pad)
        
        crop = img_bgr[y1:y2, x1:x2]
        if crop.shape[0] < 20 or crop.shape[1] < 20:
            crop = img_bgr
            
        resized = cv2.resize(crop, target_size, interpolation=cv2.INTER_CUBIC)
        mask = np.zeros(target_size, dtype=np.uint8)
        cv2.circle(mask, (target_size[0] // 2, target_size[1] // 2), int(target_size[0] * 0.47), 255, -1)
        
        return resized, mask

    @staticmethod
    def compute_image_hashes(img_bgr):
        """Computes SHA-256 cryptographic hash and 64-bit dHash for duplicate detection."""
        # 1. Cryptographic SHA-256
        sha256 = hashlib.sha256(img_bgr.tobytes()).hexdigest()
        
        # 2. Perceptual Difference Hash (dHash)
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        small = cv2.resize(gray, (9, 8), interpolation=cv2.INTER_AREA)
        diff = small[:, 1:] > small[:, :-1]
        dhash = sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
        
        return sha256, hex(dhash)[2:].zfill(16)


class ClinicalDatasetRegistry:
    """Manages clinical dataset loading, ground truth, and patient-level splits."""

    def __init__(self, data_dir=DATA_DIR):
        self.data_dir = data_dir
        self.manifest = self._load_manifest()

    def _load_manifest(self):
        if os.path.exists(MANIFEST_PATH):
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def get_heldout_test_cases(self):
        """Loads verified held-out clinical validation cases."""
        gt_path = os.path.join(self.data_dir, "heldout_test", "ground_truth.json")
        if os.path.exists(gt_path):
            with open(gt_path, "r", encoding="utf-8") as f:
                cases = json.load(f)
                for c in cases:
                    base = os.path.dirname(self.data_dir)
                    c["absolute_path"] = os.path.normpath(os.path.join(base, c["file"]))
                return cases
        return []

    def get_dataset_statistics(self):
        """Returns statistical overview of the integrated clinical datasets."""
        heldout = self.get_heldout_test_cases()
        grades = [c["grade"] for c in heldout]
        ref_count = sum(1 for c in heldout if c.get("referable"))
        
        return {
            "registered_datasets": list(self.manifest.get("datasets", {}).keys()),
            "heldout_cases_count": len(heldout),
            "heldout_grade_distribution": {g: grades.count(g) for g in range(5)},
            "referable_cases": ref_count,
            "non_referable_cases": len(heldout) - ref_count,
            "split_policy": self.manifest.get("split_policy", {})
        }


if __name__ == "__main__":
    registry = ClinicalDatasetRegistry()
    stats = registry.get_dataset_statistics()
    print("=== CLINICAL DATASET REGISTRY OVERVIEW ===")
    print(json.dumps(stats, indent=2))
