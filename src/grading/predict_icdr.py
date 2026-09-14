# -*- coding: utf-8 -*-
"""
DRISHTI AI: Single Authoritative ICDR Retinopathy Grading Engine (Backlog Items #9, #35)
"""

import os
import cv2
import numpy as np

# Import the core analyzer
from retina_analyzer import analyze_retinal_fundus

def safe_float(val, default=0.0):
    try:
        if val is None or val == 'N/A':
            return default
        return float(val)
    except (ValueError, TypeError):
        return default

def safe_int(val, default=0):
    try:
        if val is None or val == 'N/A':
            return default
        return int(val)
    except (ValueError, TypeError):
        return default

def predict_icdr_grade(img_bgr, clinical_metadata=None):
    """
    Authoritative ICDR Grade prediction function.
    """
    result = analyze_retinal_fundus(img_bgr)
    return {
        "grade": safe_int(result.get("grade", 0)),
        "grade_name": str(result.get("grade_name", "Unknown")),
        "referable": bool(result.get("referable", False)),
        "dr_damage_percentage": safe_float(result.get("dr_damage_percentage", 0.0)),
        "confidence": safe_float(result.get("dl_confidence_pct", 90.0) / 100.0, default=0.90),
        "normalized_entropy": safe_float(result.get("normalized_entropy", 0.1), default=0.1),
        "is_gradable": bool(result.get("is_gradable", True)),
        "quality_grade": str(result.get("quality_assessment", {}).get("quality_grade", "ACCEPTABLE")),
        "focus_score": safe_float(result.get("focus_score", 35.0), default=35.0),
        "glare_pct": safe_float(result.get("glare_pct", 2.0), default=2.0),
        "mas_count": safe_int(result.get("mas_count", 0)),
        "hemo_count": safe_int(result.get("hemo_count", 0)),
        "exudates_count": safe_int(result.get("exudates_count", 0)),
        "cws_count": safe_int(result.get("cws_count", 0)),
        "csme_risk": bool(result.get("csme_positive", False)),
        "csme_foveal_dist_dd": safe_float(result.get("csme_dist_dd"), default=2.0),
        "vessel_density_pct": safe_float(result.get("vessel_density_pct"), default=8.5),
        "quadrant_distribution": result.get("quadrant_distribution", {}),
        "ref_title": str(result.get("ref_title", "N/A")),
        "ref_reason": str(result.get("ref_reason", "N/A")),
        "gradcam_base64": result.get("gradcam_base64"),
        "gradcam_pp_base64": result.get("gradcam_pp_base64"),
        "dl_probs": result.get("dl_probs_calibrated") or result.get("dl_probs") or [0.2]*5
    }
