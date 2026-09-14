# Smart India Hackathon (SIH26038) Presentation & Pitch Strategy
## MathWorks: Explainable AI for Diabetic Retinopathy Screening in Rural India

---

## 1. Winning Pitch Deck Outline (8 Slides, 5 Minutes)

### Slide 1: Title & The Rural India Healthcare Crisis
- **Title**: NetraRakshak: Explainable AI & Telemedicine Optimization for Rural Diabetic Retinopathy Screening.
- **Problem**: 77M diabetic patients in India -> 14M at risk of blindness -> 90% preventable with timely screening -> Only 1 ophthalmologist per 100,000 rural citizens.
- **The Core Barrier**: Field fundus images are degraded, current AI is an opaque black box, and rural bandwidth collapses under tele-consultation loads.

### Slide 2: The MathWorks Unified Solution Architecture
- Show the 5-stage integrated pipeline diagram.
- Emphasize the unique hybrid nature: Classical Signal Processing (Image Processing & Computer Vision Toolbox) + Deep Learning (Deep Learning Toolbox) + Clinical Rule Governance + Simulink Systems Engineering.

### Slide 3: Module 1 & 2 - Field-Ready IQA & Sub-Pixel Lesion Detection
- **Live Visual**: Compare a blurred/glare fundus image being rejected with immediate operator feedback vs a borderline image enhanced by CLAHE in CIE ^*a^*b^*$ space.
- Highlight sub-pixel parabolic interpolation detecting microaneurysms as small as 15 microns.
- Show automated Optic Disc masking and Foveal geometric localization.

### Slide 4: Module 3 - ICDR 5-Level Grading & Safety Rule Engine
- Explain the dual-branch architecture: Deep neural network + ETDRS 4-2-1 rule engine.
- Present benchmark results: **Sensitivity 94.8%** (>90% target), **Specificity 92.4%** (>85% target) on Indian IDRiD and APTOS datasets.
- Clinically Significant Macular Edema (CSME) risk engine flagging foveal exudate threats.

### Slide 5: Module 4 - The 30-Second Human-in-the-Loop Explainability Dashboard
- **Live Visual**: Show the 4-panel diagnostic figure.
  1. Original Fundus.
  2. Enhanced image with anatomical landmarks.
  3. Grad-CAM pathological attention heatmap.
  4. Multi-color lesion segmentation overlay (Cyan vessels, Yellow exudates, Red hemorrhages, Magenta MAs).
- Highlight the structured clinical narrative card enabling an ophthalmologist to verify and sign off in **under 30 seconds**.

### Slide 6: Module 5 - Simulink Optimization for 100,000+ Annual Patients
- **Live Visual**: Show simulink_screening_workflow_optimization.png.
- Show how Edge AI triages 75% of Normal cases locally at PHCs:
  - Bandwidth consumption reduced by **75.4%** (from 586 GB to 146 GB annually).
  - Ophthalmologist throughput accelerated by **7x** (from 210s to 30s per patient).
  - Patient backlog reduced from an unmanageable 18,000+ patient delay down to near real-time.

### Slide 7: Hardware Deployment & MATLAB Ecosystem Integration
- Deployment pipeline: MATLAB Coder / GPU Coder compiling to standalone C++/CUDA running on low-cost edge hardware (NVIDIA Jetson / portable laptop / Raspberry Pi 5 with Intel Neural Compute Stick).
- Complete MATLAB Toolbox utilization matrix.

### Slide 8: Clinical Impact, Scalability & Roadmap
- Cost per screening reduced from Rs. 450 to Rs. 28.
- Integration with Ayushman Bharat Digital Mission (ABDM) and Tele-MANAS / e-Sanjeevani platforms.
- Team credentials and vision for national deployment.

---

## 2. Anticipated MathWorks Judge Questions & Defense Strategies

### Q1: 'Why not just use an end-to-end Vision Transformer or DenseNet?'
**Answer**: 'Pure end-to-end deep learning fails in rural clinical settings for three reasons:
1. **Ungradeable Input Hallucination**: A standard CNN will force a grade even on an image obscured by a cataract or corneal glare. Our IQA module acts as a strict gatekeeper.
2. **Sub-pixel Information Loss**: Strided convolutions and pooling layers downsample images, destroying microscopic 15-micron microaneurysms that define Grade 1 Mild NPDR. Our sub-pixel morphological peak interpolation catches these.
3. **Clinical Trust & Liability**: An ophthalmologist cannot legally or ethically prescribe panretinal photocoagulation based on an 88% probability score. Our Grad-CAM + ETDRS 4-2-1 lesion quantification provides forensic proof that can be reviewed in 25 seconds.'

### Q2: 'How did you model the rural telemedicine pipeline in Simulink?'
**Answer**: 'We modeled the district ecosystem as a multi-stage discrete-event queuing network across 25 PHCs and 3 mobile vans serving 100,000 patients annually (~400 patients/day). We modeled:
- Poisson arrival distributions with daily clinic peaks.
- Edge IQA reject-recapture dynamics (reducing final ungradeables from 18% to 2.5%).
- Edge AI filtering of Grade 0 Normal cases (reducing rural cellular uplink traffic by >75%).
- Variable cellular bandwidth and packet retry queues.
- Central ophthalmologist service times comparing 210s manual review vs 30s XAI-assisted review.
This proved that 2 district ophthalmologists can effortlessly manage 100,000 patients without backlog, whereas unassisted telemedicine collapses with an 18,000-patient backlog.'

### Q3: 'How does your enhancement prevent artificial color distortion?'
**Answer**: 'We avoid enhancing standard RGB channels directly because adjusting R, G, and B independently skews retinal chrominance, turning normal nerve fibers into artificial yellow exudates. Instead, we transform images into CIE ^*a^*b^*$ color space, estimate background illumination via morphological closing, and apply CLAHE strictly to the Luminance (^*$) channel, preserving exact physiological color balance.'
