import os

html_code = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NetraRakshak | Explainable AI Retinal Screening (MathWorks SIH26038)</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0b0f19;
            --card-bg: #131b2e;
            --card-border: #1e293b;
            --accent-blue: #0284c7;
            --accent-cyan: #06b6d4;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        header {
            background: linear-gradient(90deg, #0f172a 0%, #1e1b4b 100%);
            border-bottom: 1px solid #334155;
            padding: 16px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .brand { display: flex; align-items: center; gap: 14px; }
        .brand-logo {
            width: 44px; height: 44px;
            background: linear-gradient(135deg, #0284c7, #38bdf8);
            border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            font-size: 22px; font-weight: bold; color: white;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
        }
        .brand-text h1 { font-size: 20px; font-weight: 700; letter-spacing: -0.5px; }
        .brand-text p { font-size: 12px; color: var(--accent-cyan); font-weight: 500; }
        .header-badges { display: flex; gap: 10px; }
        .badge {
            background: rgba(255,255,255,0.07);
            border: 1px solid rgba(255,255,255,0.12);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            display: flex; align-items: center; gap: 6px;
        }
        .badge-pulse {
            width: 8px; height: 8px; border-radius: 50%;
            background: var(--success);
            box-shadow: 0 0 8px var(--success);
        }
        
        .main-layout {
            display: grid;
            grid-template-columns: 320px 1fr;
            flex: 1;
            height: calc(100vh - 77px);
        }
        
        /* SIDEBAR */
        .sidebar {
            background-color: #0f172a;
            border-right: 1px solid #1e293b;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .section-title {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #64748b;
            font-weight: 700;
            margin-bottom: 12px;
        }
        .patient-list { display: flex; flex-direction: column; gap: 10px; }
        .patient-btn {
            background: #1e293b;
            border: 1px solid #334155;
            padding: 12px 14px;
            border-radius: 10px;
            color: var(--text-primary);
            text-align: left;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .patient-btn:hover {
            border-color: var(--accent-cyan);
            transform: translateX(3px);
            background: #25334d;
        }
        .patient-btn.active {
            border-color: var(--accent-cyan);
            background: linear-gradient(135deg, rgba(2, 132, 199, 0.2), rgba(6, 182, 212, 0.1));
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.2);
        }
        .btn-top { display: flex; justify-content: space-between; align-items: center; }
        .btn-id { font-weight: 700; font-size: 13px; font-family: 'JetBrains Mono', monospace; }
        .btn-tag {
            font-size: 10px;
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 700;
        }
        .tag-grade-0 { background: rgba(16, 185, 129, 0.2); color: #34d399; }
        .tag-grade-1 { background: rgba(56, 189, 248, 0.2); color: #38bdf8; }
        .tag-grade-2 { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
        .tag-grade-3 { background: rgba(239, 68, 68, 0.2); color: #f87171; }
        .tag-grade-4 { background: rgba(225, 29, 72, 0.3); color: #fb7185; }
        .tag-reject  { background: rgba(239, 68, 68, 0.3); color: #f87171; border: 1px dashed #ef4444; }
        .btn-desc { font-size: 11px; color: var(--text-secondary); }
        
        /* CONTENT AREA */
        .content {
            padding: 24px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 24px;
        }
        
        .tabs {
            display: flex;
            gap: 12px;
            border-bottom: 1px solid #1e293b;
            padding-bottom: 12px;
        }
        .tab-btn {
            background: none;
            border: none;
            color: #94a3b8;
            font-size: 14px;
            font-weight: 600;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .tab-btn:hover { color: white; background: #1e293b; }
        .tab-btn.active { color: white; background: var(--accent-blue); }
        
        /* TRIAGE CARD & IMAGE GRID */
        .triage-banner {
            background: #131b2e;
            border: 1px solid #1e293b;
            border-radius: 14px;
            padding: 20px;
            display: grid;
            grid-template-columns: 1fr 340px;
            gap: 20px;
            align-items: center;
        }
        .triage-info h2 { font-size: 22px; font-weight: 800; margin-bottom: 8px; display: flex; align-items: center; gap: 10px; }
        .triage-info p { font-size: 14px; color: #cbd5e1; line-height: 1.5; }
        .triage-actions {
            background: #0b1120;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            text-align: center;
        }
        .conf-badge {
            font-size: 26px;
            font-weight: 800;
            color: var(--accent-cyan);
            font-family: 'JetBrains Mono', monospace;
        }
        .conf-label { font-size: 11px; text-transform: uppercase; color: #64748b; letter-spacing: 0.5px; }
        .action-btn {
            background: linear-gradient(135deg, #0284c7, #0369a1);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
        }
        .action-btn:hover { opacity: 0.9; transform: translateY(-1px); }
        
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }
        .kpi-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 16px;
        }
        .kpi-title { font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 700; }
        .kpi-val { font-size: 24px; font-weight: 800; margin: 4px 0; font-family: 'JetBrains Mono', monospace; }
        .kpi-sub { font-size: 12px; color: var(--text-secondary); }
        
        .image-viewer {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 14px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .image-viewer-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .image-viewer-header h3 { font-size: 16px; font-weight: 700; }
        .report-img {
            width: 100%;
            max-height: 680px;
            object-fit: contain;
            border-radius: 10px;
            background: #000;
            border: 1px solid #1e293b;
        }
        
        .sim-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
        }
        .sim-box {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }
        .sim-num { font-size: 36px; font-weight: 800; font-family: 'JetBrains Mono', monospace; }
        .sim-desc { font-size: 13px; color: #94a3b8; margin-top: 6px; }
        
        .tab-pane { display: none; }
        .tab-pane.active { display: flex; flex-direction: column; gap: 20px; }
        
        /* SIGN-OFF STAMP */
        .signoff-stamp {
            display: none;
            border: 2px dashed #10b981;
            color: #10b981;
            padding: 8px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1px;
            text-align: center;
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
    </style>
</head>
<body>

    <header>
        <div class="brand">
            <div class="brand-logo">N</div>
            <div class="brand-text">
                <h1>NetraRakshak Web Portal</h1>
                <p>Explainable AI for Diabetic Retinopathy Screening | MathWorks SIH26038</p>
            </div>
        </div>
        <div class="header-badges">
            <div class="badge"><div class="badge-pulse"></div> PHC Node Active</div>
            <div class="badge">District: Nanded Rural Cohort</div>
            <div class="badge">Inference: Edge MATLAB Coder Runtime</div>
        </div>
    </header>

    <div class="main-layout">
        <!-- SIDEBAR -->
        <div class="sidebar">
            <div>
                <div class="section-title">Patient Test Cohort</div>
                <div class="patient-list">
                    <button class="patient-btn active" onclick="selectPatient(0)">
                        <div class="btn-top">
                            <span class="btn-id">PAT_001_NORMAL</span>
                            <span class="btn-tag tag-grade-0">Grade 0</span>
                        </div>
                        <div class="btn-desc">No DR / Normal Healthy Retina</div>
                    </button>
                    
                    <button class="patient-btn" onclick="selectPatient(1)">
                        <div class="btn-top">
                            <span class="btn-id">PAT_002_MILD</span>
                            <span class="btn-tag tag-grade-1">Grade 1</span>
                        </div>
                        <div class="btn-desc">Mild NPDR (8 Microaneurysms)</div>
                    </button>

                    <button class="patient-btn" onclick="selectPatient(2)">
                        <div class="btn-top">
                            <span class="btn-id">PAT_003_MODERATE</span>
                            <span class="btn-tag tag-grade-2">Grade 2</span>
                        </div>
                        <div class="btn-desc">Moderate NPDR (CSME Positive)</div>
                    </button>

                    <button class="patient-btn" onclick="selectPatient(3)">
                        <div class="btn-top">
                            <span class="btn-id">PAT_004_SEVERE</span>
                            <span class="btn-tag tag-grade-3">Grade 3</span>
                        </div>
                        <div class="btn-desc">Severe NPDR (ETDRS 4-2-1 Rule)</div>
                    </button>

                    <button class="patient-btn" onclick="selectPatient(4)">
                        <div class="btn-top">
                            <span class="btn-id">PAT_005_PDR</span>
                            <span class="btn-tag tag-grade-4">Grade 4</span>
                        </div>
                        <div class="btn-desc">Proliferative DR (Neovascularization)</div>
                    </button>

                    <button class="patient-btn" onclick="selectPatient(5)">
                        <div class="btn-top">
                            <span class="btn-id">PAT_006_BLURRED</span>
                            <span class="btn-tag tag-reject">Ungradeable</span>
                        </div>
                        <div class="btn-desc">Edge IQA Reject & Recapture Advice</div>
                    </button>
                </div>
            </div>

            <div style="margin-top: auto; padding-top: 16px; border-top: 1px solid #1e293b;">
                <div class="section-title">Validation Metrics</div>
                <div style="font-size: 12px; color: #94a3b8; display: flex; flex-direction: column; gap: 6px;">
                    <div>Sensitivity (Referable): <b style="color: #38bdf8;">94.8%</b> (Target >90%)</div>
                    <div>Specificity (Referable): <b style="color: #34d399;">92.4%</b> (Target >85%)</div>
                    <div>Validation Speed: <b style="color: #fbbf24;">&lt; 30 Seconds</b></div>
                </div>
            </div>
        </div>

        <!-- MAIN CONTENT AREA -->
        <div class="content">
            <div class="tabs">
                <button class="tab-btn active" onclick="switchTab('triage')">Clinical Triage & Explainability (XAI)</button>
                <button class="tab-btn" onclick="switchTab('simulink')">Simulink Telemedicine Optimization (100k Patients)</button>
                <button class="tab-btn" onclick="switchTab('architecture')">MathWorks Toolboxes & Architecture</button>
            </div>

            <!-- TAB 1: CLINICAL TRIAGE -->
            <div id="tab-triage" class="tab-pane active">
                <div class="triage-banner" id="triageBanner">
                    <div class="triage-info">
                        <h2 id="patientTitle">Grade 0: Normal Retina <span class="btn-tag tag-grade-0" id="referableBadge">NON-REFERABLE</span></h2>
                        <p id="clinicalRationale">No microaneurysms, intraretinal hemorrhages, hard exudates, or neovascularization observed. Normal retinal microvasculature with intact foveal avascular zone.</p>
                        <p style="margin-top: 8px; font-weight: 600; color: #38bdf8;" id="clinicalAction">Recommendation: Routine annual tele-screening at local Primary Health Centre (PHC).</p>
                    </div>
                    <div class="triage-actions">
                        <div class="conf-badge" id="confScore">98.6%</div>
                        <div class="conf-label">Calibrated Confidence (T=1.2)</div>
                        <button class="action-btn" id="signOffBtn" onclick="signOffCase()">Sign-Off Diagnosis (&lt;30s)</button>
                        <div class="signoff-stamp" id="signoffStamp">VERIFIED & SIGNED BY OPHTHALMOLOGIST</div>
                    </div>
                </div>

                <!-- KPI SCORECARDS -->
                <div class="kpi-grid">
                    <div class="kpi-card">
                        <div class="kpi-title">Image Quality (IQA)</div>
                        <div class="kpi-val" style="color: #34d399;" id="iqaScore">64.8</div>
                        <div class="kpi-sub" id="iqaSub">Tenengrad Focus (>15.0) | Glare: 1.8%</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-title">Microaneurysms (MAs)</div>
                        <div class="kpi-val" style="color: #38bdf8;" id="maCount">0</div>
                        <div class="kpi-sub">Sub-Pixel Parabolic Peak Interpolation</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-title">Hemorrhages & 4-2-1 Rule</div>
                        <div class="kpi-val" style="color: #fb7185;" id="hemoCount">0</div>
                        <div class="kpi-sub" id="hemoSub">4-Quadrant Distribution</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-title">Macular Edema (CSME) Risk</div>
                        <div class="kpi-val" style="color: #fbbf24;" id="csmeRisk">None</div>
                        <div class="kpi-sub" id="csmeSub">Distance to Foveal Center</div>
                    </div>
                </div>

                <!-- 4-PANEL OPHTHALMOLOGIST VALIDATION FIGURE -->
                <div class="image-viewer">
                    <div class="image-viewer-header">
                        <h3>Ophthalmologist Rapid Validation Console (4-Panel Multimodal Display)</h3>
                        <span style="font-size: 12px; color: #94a3b8;">Original | Enhanced & Landmarks | Grad-CAM Attention Heatmap | Color-Coded Lesion Overlay</span>
                    </div>
                    <img id="reportImage" class="report-img" src="/results/screening_report_PAT_001_NORMAL.png" alt="Clinical Report Figure">
                </div>
            </div>

            <!-- TAB 2: SIMULINK OPTIMIZATION -->
            <div id="tab-simulink" class="tab-pane">
                <div class="sim-grid">
                    <div class="sim-box">
                        <div class="sim-num" style="color: #34d399;">75.0%</div>
                        <div class="sim-desc">Rural Bandwidth Saved via Edge AI Triage (575 GB down to 144 GB)</div>
                    </div>
                    <div class="sim-box">
                        <div class="sim-num" style="color: #38bdf8;">7.0x</div>
                        <div class="sim-desc">Doctor Throughput Multiplier (30s vs 210s Manual Review)</div>
                    </div>
                    <div class="sim-box">
                        <div class="sim-num" style="color: #fbbf24;">0 Backlog</div>
                        <div class="sim-desc">Zero Patient Delay vs 49,265 Patient Queue in Traditional Model</div>
                    </div>
                </div>

                <div class="image-viewer">
                    <div class="image-viewer-header">
                        <h3>Simulink Discrete-Event Simulation: 100,000 Annual Diabetic Patients</h3>
                        <span style="font-size: 12px; color: #94a3b8;">250 Operational Days | 25 Primary Health Centres & Mobile Vans | 2 District Ophthalmologists</span>
                    </div>
                    <img class="report-img" src="/results/simulink_screening_workflow_optimization.png" alt="Simulink Optimization Results">
                </div>
            </div>

            <!-- TAB 3: ARCHITECTURE & TOOLBOXES -->
            <div id="tab-architecture" class="tab-pane">
                <div class="triage-banner" style="grid-template-columns: 1fr;">
                    <h2 style="color: var(--accent-cyan);">MathWorks Toolboxes Technical Integration Matrix</h2>
                    <p style="margin-top: 10px; line-height: 1.8;">
                        • <b>Image Processing Toolbox</b>: Retinal Field-of-View (FoV) circular mask extraction, morphological top-hat & bottom-hat operators, CIE L*a*b* color transformation, Contrast-Limited Adaptive Histogram Equalization (<code style="color: #38bdf8;">adapthisteq</code>), edge-preserving bilateral filtering (<code style="color: #38bdf8;">imbilatfilt</code>), and Circular Hough Transform.<br>
                        • <b>Computer Vision Toolbox</b>: Spatial geometric landmarking for Optic Disc and Foveal center avascular zone, sub-pixel parabolic peak interpolation for capillary microaneurysms (<code style="color: #38bdf8;">15 μm</code> accuracy).<br>
                        • <b>Deep Learning Toolbox</b>: Gradient-weighted Class Activation Mapping (<code style="color: #38bdf8;">Grad-CAM</code>) extracting deep feature attention overlays for transparent human-in-the-loop verification.<br>
                        • <b>Statistics and Machine Learning Toolbox</b>: Temperature-scaled posterior confidence calibration (<code style="color: #38bdf8;">T = 1.2</code>, ECE &lt; 0.03), 4-quadrant ETDRS lesion clustering, Poisson patient arrival distribution.<br>
                        • <b>Simulink & SimEvents</b>: Discrete-event multi-stage queuing simulation modeling 100,000 rural diabetic patients across 25 PHCs, channel bandwidth limits, and doctor validation capacity.
                    </p>
                </div>
            </div>
        </div>
    </div>

    <script>
        const patients = [
            {
                id: "PAT_001_NORMAL",
                title: "Grade 0: Normal Retina",
                badge: "NON-REFERABLE",
                badgeClass: "tag-grade-0",
                rationale: "No microaneurysms, intraretinal hemorrhages, hard exudates, or neovascularization observed. Normal retinal microvasculature with intact foveal avascular zone.",
                action: "Recommendation: Routine annual tele-screening at local Primary Health Centre (PHC).",
                conf: "98.6%",
                iqa: "64.8",
                iqaSub: "Tenengrad Focus (>15.0) | Glare: 1.8%",
                mas: "0",
                hemo: "0",
                hemoSub: "4-Quadrant Distribution",
                csme: "None",
                csmeSub: "Distance to Foveal Center: >10 DD",
                img: "/results/screening_report_PAT_001_NORMAL.png"
            },
            {
                id: "PAT_002_MILD",
                title: "Grade 1: Mild NPDR",
                badge: "NON-REFERABLE",
                badgeClass: "tag-grade-1",
                rationale: "Isolated sub-pixel microaneurysms (8 detected) only. Foveal avascular zone preserved; no exudates, hemorrhages, or venous beading present.",
                action: "Recommendation: Annual routine tele-retinal screening. Reinforce glycemic and lifestyle control at local PHC.",
                conf: "92.1%",
                iqa: "182.4",
                iqaSub: "Tenengrad Focus (>15.0) | Glare: 2.1%",
                mas: "8",
                hemo: "0",
                hemoSub: "4-Quadrant Distribution",
                csme: "None",
                csmeSub: "Distance to Foveal Center: >10 DD",
                img: "/results/screening_report_PAT_002_MILD.png"
            },
            {
                id: "PAT_003_MODERATE",
                title: "Grade 2: Moderate NPDR",
                badge: "REFERABLE (URGENT DME)",
                badgeClass: "tag-grade-2",
                rationale: "Multiple microaneurysms (19) and intraretinal blot hemorrhages (18) detected. Hard exudates present within 0.12 Disc Diameters of the foveal center, indicating Clinically Significant Macular Edema (CSME).",
                action: "Recommendation: Prompt referral to Ophthalmologist within 1-2 weeks for optical coherence tomography (OCT) and Anti-VEGF evaluation.",
                conf: "91.5%",
                iqa: "848.6",
                iqaSub: "Tenengrad Focus (>15.0) | Glare: 3.2%",
                mas: "19",
                hemo: "18",
                hemoSub: "4-Quadrant Distribution",
                csme: "HIGH RISK",
                csmeSub: "Distance to Fovea: 0.12 DD (<1.0 DD)",
                img: "/results/screening_report_PAT_003_MODERATE.png"
            },
            {
                id: "PAT_004_SEVERE",
                title: "Grade 3: Severe NPDR",
                badge: "REFERABLE (HIGH PRIORITY)",
                badgeClass: "tag-grade-3",
                rationale: "Fulfilled ETDRS 4-2-1 criteria: >=20 intraretinal hemorrhages detected across all 4 quadrants (Total hemorrhages: 88, MAs: 40). ~50% risk of progression to proliferative retinopathy within 1 year.",
                action: "Recommendation: Refer to Ophthalmologist within 2-4 weeks. Intensive monitoring and strict HbA1c optimization.",
                conf: "94.2%",
                iqa: "1343.5",
                iqaSub: "Tenengrad Focus (>15.0) | Glare: 3.6%",
                mas: "40",
                hemo: "88",
                hemoSub: "Severe: >=20 in All 4 Quadrants",
                csme: "HIGH RISK",
                csmeSub: "Distance to Fovea: 0.09 DD",
                img: "/results/screening_report_PAT_004_SEVERE.png"
            },
            {
                id: "PAT_005_PDR",
                title: "Grade 4: Proliferative DR (PDR)",
                badge: "REFERABLE (EMERGENT)",
                badgeClass: "tag-grade-4",
                rationale: "Definite Neovascularization of the Disc (NVD) detected at optic disc margin with abnormal vessel branching loops. Severe risk of vitreous hemorrhage, tractional retinal detachment, and irreversible blindness.",
                action: "EMERGENT: Immediate referral to Vitreoretinal Specialist within 48-72 hours for Panretinal Photocoagulation (PRP) or Anti-VEGF therapy.",
                conf: "97.4%",
                iqa: "1560.9",
                iqaSub: "Tenengrad Focus (>15.0) | Glare: 3.9%",
                mas: "44",
                hemo: "95",
                hemoSub: "Severe: 95 Hemorrhages",
                csme: "HIGH RISK",
                csmeSub: "Distance to Fovea: 0.25 DD",
                img: "/results/screening_report_PAT_005_PDR.png"
            },
            {
                id: "PAT_006_BLURRED",
                title: "Image Rejected: Field Failure",
                badge: "RECAPTURE REQUIRED",
                badgeClass: "tag-reject",
                rationale: "Image Quality Assessment (IQA) Failure: Severe motion blur (Tenengrad focus 7.4 < 15.0 threshold) and excessive corneal reflection glare (18.5% area > 15.0% limit). Downstream AI inference safely halted at edge.",
                action: "Edge Operator Guidance: Clean lens, steady patient head on chin rest, tilt camera 5 degrees away from corneal glare reflection, and recapture.",
                conf: "0.0%",
                iqa: "7.40",
                iqaSub: "BELOW THRESHOLD (<15.0) | Glare: 18.5%",
                mas: "-",
                hemo: "-",
                hemoSub: "Inference Halted",
                csme: "Ungradeable",
                csmeSub: "Recapture in Progress",
                img: "/results/screening_report_PAT_006_BLURRED.png"
            }
        ];

        let currentIndex = 0;

        function selectPatient(index) {
            currentIndex = index;
            const p = patients[index];
            
            // Buttons active state
            const btns = document.querySelectorAll('.patient-btn');
            btns.forEach((b, i) => b.classList.toggle('active', i === index));

            // Update Triage Banner
            document.getElementById('patientTitle').innerHTML = `${p.title} <span class="btn-tag ${p.badgeClass}" id="referableBadge">${p.badge}</span>`;
            document.getElementById('clinicalRationale').innerText = p.rationale;
            document.getElementById('clinicalAction').innerText = p.action;
            document.getElementById('confScore').innerText = p.conf;

            // KPIs
            document.getElementById('iqaScore').innerText = p.iqa;
            document.getElementById('iqaSub').innerText = p.iqaSub;
            document.getElementById('maCount').innerText = p.mas;
            document.getElementById('hemoCount').innerText = p.hemo;
            document.getElementById('hemoSub').innerText = p.hemoSub;
            document.getElementById('csmeRisk').innerText = p.csme;
            document.getElementById('csmeSub').innerText = p.csmeSub;

            // Report Image
            document.getElementById('reportImage').src = p.img;

            // Reset stamp
            document.getElementById('signoffStamp').style.display = 'none';
            document.getElementById('signOffBtn').style.display = 'block';
        }

        function signOffCase() {
            document.getElementById('signoffStamp').style.display = 'block';
            document.getElementById('signOffBtn').style.display = 'none';
        }

        function switchTab(tabId) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

            if (tabId === 'triage') {
                document.querySelector('.tab-btn:nth-child(1)').classList.add('active');
                document.getElementById('tab-triage').classList.add('active');
            } else if (tabId === 'simulink') {
                document.querySelector('.tab-btn:nth-child(2)').classList.add('active');
                document.getElementById('tab-simulink').classList.add('active');
            } else if (tabId === 'architecture') {
                document.querySelector('.tab-btn:nth-child(3)').classList.add('active');
                document.getElementById('tab-architecture').classList.add('active');
            }
        }
    </script>
</body>
</html>
"""

with open("web/index.html", "w", encoding="utf-8") as f:
    f.write(html_code)
print("Created web/index.html successfully!")
