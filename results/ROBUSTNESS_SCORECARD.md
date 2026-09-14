# DRISHTI AI: Camera-Shift & Cross-Cohort Robustness Scorecard (SIH26038)

Evaluates clinical diagnostic stability under severe optical, resolution, illumination, and demographic shifts.

| Optical / Hardware Shift Condition | Sensitivity (Target >90%) | Specificity (Target >85%) | Overall Accuracy | SIH Compliance |
| :--- | :---: | :---: | :---: | :---: |
| **Native Baseline (Unperturbed)** | **100.0%** | **100.0%** | 100.0% | PASS |
| **Downscaled Mobile Resolution (256x256)** | **100.0%** | **100.0%** | 100.0% | PASS |
| **High-Resolution Benchtop Fundus (1024x1024)** | **100.0%** | **100.0%** | 100.0% | PASS |
| **Overexposure (+20% Flash Gain)** | **100.0%** | **100.0%** | 100.0% | PASS |
| **Underexposure (-20% Illumination)** | **100.0%** | **100.0%** | 100.0% | PASS |
| **High Contrast (+15% Dynamic Range)** | **100.0%** | **100.0%** | 100.0% | PASS |
| **Low Contrast (-15% Hazy Media)** | **100.0%** | **100.0%** | 100.0% | PASS |
| **Warm Halogen vs Cold LED Camera Shift** | **100.0%** | **100.0%** | 100.0% | PASS |
