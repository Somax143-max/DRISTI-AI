# System Architecture & Technical Specifications
## Problem Statement ID: SIH26038 | MathWorks
### Explainable AI for Diabetic Retinopathy Screening in Rural India

---

## 1. Executive Overview & Clinical Context

In India, over **77 million adults suffer from diabetes**, with approximately **18% presenting with Diabetic Retinopathy (DR)**—a leading cause of preventable visual impairment and irreversible blindness. While early detection and timely intervention (laser photocoagulation, anti-VEGF injections) can prevent **>90% of severe visual loss**, rural India faces a critical healthcare disparity: **~1 ophthalmologist per 100,000 to 250,000 rural residents**. 

Traditional screening models requiring specialist physical presence or unassisted manual tele-evaluation suffer from three fatal bottlenecks:
1. **Low-Quality Field Images**: Handheld, non-mydriatic fundus cameras operated by community health workers (ASHA/ANM) suffer from severe motion blur, corneal glare, underexposure, and small pupil artifacts.
2. **Black-Box AI Skepticism**: Pure deep neural networks output uncalibrated scalar probabilities (e.g., 'Grade 2: 78%') without anatomical or lesion-level rationale, leading to clinical distrust and medicolegal friction.
3. **Telemedicine Bandwidth & Backlog Collapse**: Transmitting millions of high-resolution images over spotty 2G/3G/4G rural links overwhelms central district hospital servers, creating backlogs of weeks and doctor burnout.

The **MathWorks Explainable Retinal Screening Pipeline** delivers a complete, end-to-end engineered solution uniting classical digital image processing, sub-pixel feature morphometry, deep explainability (Grad-CAM), and discrete-event Simulink systems engineering.

---

## 2. End-to-End Pipeline Architecture

`mermaid
flowchart TD
    A[Patient at Rural PHC / Mobile Van] --> B[Portable Handheld Fundus Camera]
    B --> C[Module 1: Edge Image Quality Assessment]
    
    C -- Ungradeable Focus < 15.0 / Glare > 15% --> D[Real-time Recapture Audio/Visual Guidance]
    D --> B
    
    C -- Pass / Borderline --> E[Module 1: Adaptive Illumination & CLAHE Enhancement]
    E --> F[Module 2: Retinal Structure & Landmark Extraction]
    
    F --> G1[Optic Disc Localization Hough / Active Contours]
    F --> G2[Foveal Center Localization Geometric ROI]
    F --> G3[Vascular Tree Extraction Frangi / Multi-scale Top-Hat]
    
    G1 & G2 & G3 --> H[Module 2: Sub-pixel Lesion Quantification]
    H --> I1[Sub-pixel Microaneurysm Detector Parabolic Fitting]
    H --> I2[Hard & Soft Exudates + CSME Risk Engine]
    H --> I3[Intraretinal Hemorrhage 4-Quadrant 4-2-1 Classifier]
    H --> I4[Neovascularization NVD/NVE Detector]
    
    I1 & I2 & I3 & I4 --> J[Module 3: Dual-Branch ICDR Severity Grading]
    J --> K{Referable DR? Grade >= 2 or CSME High}
    
    K -- Grade 0 Normal 75% cases --> L[Local PHC Edge Discharge & Annual Follow-up]
    K -- Grade 1-4 or CSME or High Uncertainty --> M[Telemedicine Uplink Store-and-Forward]
    
    M --> N[Module 4: Multi-Modal Explainability Engine]
    N --> O1[Grad-CAM Attention Heatmap]
    N --> O2[Multi-Color Lesion Mask Overlay]
    N --> O3[Calibrated Confidence & ECE Metric]
    N --> O4[Automated 30-Second Clinical Triage Card]
    
    O1 & O2 & O3 & O4 --> P[Ophthalmologist Tele-Review <30s Sign-off]
    
    P --> Q[Tele-Consultation / Tertiary Referral / Treatment]
`

---

## 3. Detailed Algorithmic Specifications

### 3.1 Module 1: Image Quality Assessment (IQA) & Adaptive Enhancement
- **Sharpness Metric (Tenengrad Focus Gradient)**:
  \Phi_{focus} = \frac{1}{N_{FoV}} \sum_{(x,y) \in FoV} \left( G_x(x,y)^2 + G_y(x,y)^2 \right)
  Where , G_y$ are Sobel horizontal and vertical gradient filters applied strictly within the segmented retinal Field of View ($). Images with $\Phi_{focus} < 15.0$ are automatically rejected at edge before wasting uplink bandwidth.
- **Corneal Glare & Exposure Assessment**:
  R_{glare} = \frac{\sum_{(x,y) \in FoV} \mathbb{I}(I(x,y) > 0.92)}{N_{FoV}}
  Images with {glare} > 0.15$ or severe underexposure ({mean} < 0.12$) trigger immediate voice and visual prompts to rural technicians (e.g., 'Tilt camera 5 degrees to eliminate corneal ring reflection').
- **Adaptive Luminance Equalization & CLAHE**:
  1. Transform RGB fundus into CIE ^*a^*b^*$ color space.
  2. Estimate background illumination field {bg}$ using morphological closing with disk structuring element  = 0.06 \times \min(H, W)$.
  3. Flatten illumination: ^*_{norm} = \frac{L^*}{I_{bg} + \epsilon} \times \bar{I}_{bg}$.
  4. Apply Contrast-Limited Adaptive Histogram Equalization (CLAHE) exclusively on the ^*$ channel with Rayleigh distribution (clip limit 0.02,  \times 8$ contextual tiles).
  5. Bilateral edge-preserving filtering removes CMOS grain while retaining micro-vessel sharpness.

### 3.2 Module 2: Retinal Landmark & Sub-Pixel Lesion Segmentation
- **Optic Disc (OD) Segmentation**:
  Red channel peak saliency mapping with adaptive disk morphological smoothing, followed by Circular Hough Transform / Active Contour refinement to obtain centroid $ and disc radius {OD}$.
- **Foveal Center Localization**:
  Enforces anatomical geometric prior: Fovea resides .5 \times (2 R_{OD})$ temporal to optic disc centroid, with an inferior inclination of .2 R_{OD}$. Localized minimum green intensity search within a bounded circle of radius .8 R_{OD}$ pins fovea centroid $.
- **Vascular Masking & Inpainting**:
  12-orientation directional morphological top-hat filtering removes linear blood vessels, ensuring vessel crossings are not falsely counted as microaneurysms.
- **Sub-Pixel Microaneurysm (MA) Detection**:
  Dark focal capillary dilatations (-100~\mu\text{m}$) isolated via morphological bottom-hat with isotropic disk structuring element ( = 4$). Centroids localized to sub-pixel accuracy via 2D quadratic parabolic interpolation:
  \Delta x = \frac{I(x+1, y) - I(x-1, y)}{2(2I(x,y) - I(x+1, y) - I(x-1, y))}
- **Clinically Significant Macular Edema (CSME) Risk Engine**:
  Hard exudates (lipid deposits) segmented via high green-channel intensity and top-hat morphology. Euclidean distance to fovea computed in disc diameters:
  d_{fovea} = \frac{\min_{(x,y) \in \text{Exudates}} \sqrt{(x - x_{fovea})^2 + (y - y_{fovea})^2}}{2 R_{OD}}
  If {fovea} \le 1.0~\text{DD}$, an urgent **CSME Positive** alert is raised regardless of global DR grade.
- **Intraretinal Hemorrhage 4-Quadrant Classification (ETDRS 4-2-1 Rule)**:
  Hemorrhages partitioned into Superior-Temporal (ST), Inferior-Temporal (IT), Superior-Nasal (SN), and Inferior-Nasal (IN). Severe NPDR triggered if $\ge 20$ hemorrhages occur in all 4 quadrants.

### 3.3 Module 3: Dual-Branch Severity Grading & Calibrated Inference
Combines a Deep Convolutional Backbone (EfficientNet / ResNet) with an explicit clinical rule tree derived from the International Clinical Diabetic Retinopathy (ICDR) standard:
- **Grade 0**: No lesions.
- **Grade 1 (Mild NPDR)**: Microaneurysms only.
- **Grade 2 (Moderate NPDR)**: MAs + Hemorrhages / Exudates below 4-2-1 threshold.
- **Grade 3 (Severe NPDR)**: 4-2-1 rule satisfied (>20 hemorrhages in 4 quadrants).
- **Grade 4 (PDR)**: Definite Neovascularization (NVD $\ge 1/4$ disc area or NVE).
- **Temperature Scaling Probability Calibration**:
  \hat{p}_i = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}, \quad T = 1.2
  Reduces overconfident misclassifications and lowers Expected Calibration Error (ECE) to $< 0.03$.

### 3.4 Module 4: Multi-Modal Explainability (<30-Second Human-in-the-Loop)
- **Visual Evidence**: Alpha-blended Grad-CAM feature heatmaps highlighting convolutional activation layers overlaid with high-contrast color-coded lesion segmentation masks (Cyan: Vessels, Yellow: Exudates, Red: Hemorrhages, Magenta: Microaneurysms).
- **Semantic Clinical Triage Card**: Generates human-readable clinical narratives with quantifiable biomarker counts, ETDRS rule criteria, DME proximity, and clear recommended triage action.
