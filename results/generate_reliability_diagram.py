"""
DRISHTI AI: Expected Calibration Error (ECE) & Reliability Diagram Generator (SIH26038)
Computes:
- Binned accuracy vs. confidence across 10 calibration intervals
- Expected Calibration Error (ECE) and Maximum Calibration Error (MCE)
- Plots publication-grade Reliability Diagram + Entropy Uncertainty Distribution
- Saves results/reliability_diagram.png and results/calibration_analysis.json
"""

import os, sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE_DIR = r"d:\2nd move from os\d\PRO R"
sys.path.insert(0, BASE_DIR)
import retina_analyzer

GT_PATH = os.path.join(BASE_DIR, "data", "heldout_test", "ground_truth.json")
OUT_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(OUT_DIR, exist_ok=True)

def generate_calibration_diagram():
    with open(GT_PATH, "r", encoding="utf-8") as f:
        ground_truth = json.load(f)

    confidences = []
    accuracies = []
    entropies = []
    grades_true = []
    grades_pred = []

    print(f"\n=== EVALUATING CALIBRATION ON {len(ground_truth)} HELDOUT CLINICAL SAMPLES ===")
    for case in ground_truth:
        img_path = os.path.join(BASE_DIR, case["file"])
        im = cv2.imread(img_path)
        if im is None: continue
        res = retina_analyzer.analyze_retinal_fundus(im)
        
        pred_grade = res.get("grade", 0)
        true_grade = case["grade"]
        is_correct = 1.0 if (pred_grade == true_grade) else 0.0
        
        probs = res.get("dl_probs_calibrated", res.get("dl_probs", [0.2]*5))
        top_conf = float(np.max(probs))
        entropy = float(res.get("normalized_entropy", 0.0))
        
        confidences.append(top_conf)
        accuracies.append(is_correct)
        entropies.append(entropy)
        grades_true.append(true_grade)
        grades_pred.append(pred_grade)
        print(f"File: {os.path.basename(case['file']):32} | True: {true_grade} | Pred: {pred_grade} | Top Conf: {top_conf:.4f} | Entropy: {entropy:.4f}")

    confidences = np.array(confidences)
    accuracies = np.array(accuracies)
    entropies = np.array(entropies)

    # 10 Bins
    n_bins = 10
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]

    ece = 0.0
    mce = 0.0
    bin_data = []

    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
        in_bin = (confidences > bin_lower) & (confidences <= bin_upper)
        prop_in_bin = np.mean(in_bin)
        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(accuracies[in_bin])
            avg_confidence_in_bin = np.mean(confidences[in_bin])
            abs_diff = np.abs(avg_confidence_in_bin - accuracy_in_bin)
            ece += abs_diff * prop_in_bin
            mce = max(mce, abs_diff)
            bin_data.append({
                "bin_range": [round(float(bin_lower), 2), round(float(bin_upper), 2)],
                "sample_count": int(np.sum(in_bin)),
                "prop_samples": round(float(prop_in_bin), 4),
                "avg_confidence": round(float(avg_confidence_in_bin), 4),
                "accuracy": round(float(accuracy_in_bin), 4),
                "calibration_gap": round(float(abs_diff), 4)
            })
        else:
            bin_data.append({
                "bin_range": [round(float(bin_lower), 2), round(float(bin_upper), 2)],
                "sample_count": 0,
                "prop_samples": 0.0,
                "avg_confidence": round(float((bin_lower + bin_upper) / 2.0), 4),
                "accuracy": 0.0,
                "calibration_gap": 0.0
            })

    print(f"\nExpected Calibration Error (ECE): {ece:.4f}")
    print(f"Maximum Calibration Error (MCE):  {mce:.4f}")

    # Plot Reliability Diagram
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Panel 1: Reliability Diagram
    bin_centers = (bin_boundaries[:-1] + bin_boundaries[1:]) / 2.0
    bin_accs = [b["accuracy"] for b in bin_data]
    bin_confs = [b["avg_confidence"] for b in bin_data]
    bin_counts = [b["sample_count"] for b in bin_data]

    ax1.plot([0, 1], [0, 1], linestyle="--", color="#6c757d", label="Perfect Calibration (y = x)")
    
    # Draw bars for bins with samples
    active_indices = [i for i, c in enumerate(bin_counts) if c > 0]
    if active_indices:
        ax1.bar(
            bin_centers[active_indices],
            [bin_accs[i] for i in active_indices],
            width=0.08,
            color="#0ea5e9",
            alpha=0.8,
            edgecolor="#0284c7",
            label="Outputs (Empirical Accuracy)"
        )
        # Gap representation
        for i in active_indices:
            gap = abs(bin_accs[i] - bin_confs[i])
            if gap > 0.001:
                ax1.bar(
                    bin_centers[i],
                    gap,
                    bottom=min(bin_accs[i], bin_confs[i]),
                    width=0.08,
                    color="#ef4444",
                    alpha=0.4,
                    hatch="//",
                    label="Calibration Gap" if i == active_indices[0] else ""
                )

    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1.05)
    ax1.set_xlabel("Confidence", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Accuracy", fontsize=12, fontweight="bold")
    ax1.set_title(f"DRISHTI AI: Reliability Diagram\nECE = {ece:.4f} | MCE = {mce:.4f}", fontsize=13, fontweight="bold")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left")

    # Panel 2: Uncertainty vs Diagnostic Confidence
    ax2.scatter(confidences, entropies, c="#10b981", s=90, edgecolors="#065f46", alpha=0.9, zorder=3)
    ax2.axhline(0.60, color="#f59e0b", linestyle="--", label="High Uncertainty Threshold (H > 0.60)")
    ax2.axvline(0.50, color="#ef4444", linestyle=":", label="Low Confidence Border (p < 0.50)")
    ax2.set_xlim(0, 1.05)
    ax2.set_ylim(-0.05, 1.05)
    ax2.set_xlabel("Calibrated Confidence (max prob)", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Normalized Shannon Entropy (Uncertainty)", fontsize=12, fontweight="bold")
    ax2.set_title("Diagnostic Uncertainty Distribution (XAI Safety Layer)", fontsize=13, fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="upper right")

    plt.tight_layout()
    diagram_path = os.path.join(OUT_DIR, "reliability_diagram.png")
    plt.savefig(diagram_path, dpi=200)
    plt.close()
    print(f"Reliability Diagram saved to: {diagram_path}")

    # Copy to results/generate_reliability_diagram.py
    with open(os.path.join(BASE_DIR, "results", "generate_reliability_diagram.py"), "w", encoding="utf-8") as f:
        with open(__file__, "r", encoding="utf-8") as current_f:
            f.write(current_f.read())

    # Save JSON summary
    report = {
        "expected_calibration_error": round(float(ece), 4),
        "maximum_calibration_error": round(float(mce), 4),
        "temperature_scaling_factor": 1.12,
        "n_bins": n_bins,
        "calibration_bins": bin_data,
        "cases_analyzed": len(ground_truth)
    }
    json_path = os.path.join(OUT_DIR, "calibration_analysis.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Calibration analysis JSON saved to: {json_path}\n")

if __name__ == "__main__":
    generate_calibration_diagram()
