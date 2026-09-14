# -*- coding: utf-8 -*-
"""
DRISHTI AI: Dataset Deduplication and Patient-Level Splitting (Backlog Items #1, #3)
"""

import os
import glob
import json
import hashlib
import numpy as np
from PIL import Image

def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def compute_dhash(image_path, hash_size=8):
    try:
        with Image.open(image_path) as img:
            img = img.convert('L').resize((hash_size + 1, hash_size), Image.Resampling.BILINEAR)
            pixels = np.array(img, dtype=np.float32)
            diff = pixels[:, 1:] > pixels[:, :-1]
            return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
    except Exception:
        return None

def hamming_distance(hash1, hash2):
    if hash1 is None or hash2 is None:
        return 999
    return bin(hash1 ^ hash2).count('1')

def audit_dataset_for_duplicates(dataset_dirs, similarity_threshold=4):
    exact_hashes = {}
    perceptual_hashes = {}
    duplicates = []
    perceptual_matches = []

    all_files = []
    for d in dataset_dirs:
        if os.path.exists(d):
            for ext in ('*.png', '*.jpg', '*.jpeg', '*.webp', '*.tif'):
                all_files.extend(glob.glob(os.path.join(d, ext)))

    for fpath in all_files:
        sha = compute_sha256(fpath)
        dhash = compute_dhash(fpath)

        if sha in exact_hashes:
            duplicates.append({
                "file1": exact_hashes[sha],
                "file2": fpath,
                "sha256": sha,
                "type": "EXACT_DUPLICATE"
            })
        else:
            exact_hashes[sha] = fpath

        if dhash is not None:
            for prev_dhash, prev_path in perceptual_hashes.items():
                dist = hamming_distance(dhash, prev_dhash)
                if dist <= similarity_threshold and exact_hashes.get(sha) != prev_path:
                    perceptual_matches.append({
                        "file1": prev_path,
                        "file2": fpath,
                        "hamming_dist": dist,
                        "type": "PERCEPTUAL_NEAR_DUPLICATE"
                    })
            perceptual_hashes[dhash] = fpath

    return {
        "total_images_analyzed": len(all_files),
        "exact_duplicates": duplicates,
        "perceptual_near_duplicates": perceptual_matches,
        "clean_unique_images_count": len(exact_hashes)
    }
