# -*- coding: utf-8 -*-
"""
DRISHTI AI: Confidence Calibration & Reliability Metrics (Backlog Items #10, #31)
"""

import numpy as np

def compute_ece(probs, labels, n_bins=10):
    """
    Computes Expected Calibration Error (ECE) and bin details.
    """
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    confidences = np.max(probs, axis=1)
    predictions = np.argmax(probs, axis=1)
    accuracies = predictions == labels

    ece = 0.0
    bin_details = []

    for i in range(n_bins):
        in_bin = (confidences > bin_boundaries[i]) & (confidences <= bin_boundaries[i + 1])
        prop_in_bin = np.mean(in_bin)
        if prop_in_bin > 0:
            acc_bin = np.mean(accuracies[in_bin])
            conf_bin = np.mean(confidences[in_bin])
            ece += np.abs(acc_bin - conf_bin) * prop_in_bin
            bin_details.append({
                "bin_range": [round(float(bin_boundaries[i]), 2), round(float(bin_boundaries[i+1]), 2)],
                "accuracy": round(float(acc_bin), 4),
                "confidence": round(float(conf_bin), 4),
                "count": int(np.sum(in_bin))
            })

    return round(float(ece), 4), bin_details
